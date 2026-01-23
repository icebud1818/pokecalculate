let products = [];
let filteredProducts = [];
let activeFilter = "all";
let lastSortCriteria = "nameAsc";

// Fetch sealed products data from Firebase Firestore
async function fetchProducts() {
    console.log("Starting to fetch sealed products...");
    
    try {
        // Wait for Firebase to be initialized
        let attempts = 0;
        while (!window.db || !window.collection || !window.getDocs) {
            console.log("Waiting for Firebase to initialize...", attempts);
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
            
            if (attempts > 50) {
                throw new Error("Firebase failed to initialize after 5 seconds");
            }
        }

        console.log("Firebase initialized, fetching sealedProducts collection...");
        const querySnapshot = await window.getDocs(window.collection(window.db, "sealedProducts"));
        console.log("Sealed products query snapshot received, size:", querySnapshot.size);
        
        const data = [];
        
        querySnapshot.forEach((doc) => {
            console.log("Sealed product document data:", doc.id, doc.data());
            data.push({
                id: doc.id,
                ...doc.data()
            });
        });

        console.log("Total sealed products fetched:", data.length);
        initializeProducts(data);
    } catch (error) {
        handleError(error);
    }
}

function initializeProducts(data) {
    products = data.map((item) => {
        const totalValue = item.packTotal + (item.promoPrice || 0);
        const percentProfit = item.price > 0 ? ((totalValue - item.price) / item.price) * 100 : 0;
        
        return {
            id: item.id,
            productId: item.productId,
            name: item.name,
            price: item.price,
            promoPrice: item.promoPrice || 0,
            packTotal: item.packTotal,
            totalValue: totalValue,
            percentProfit: percentProfit,
            packs: item.packs || [],
            promos: item.promos || [],
            releaseDate: item.releaseDate,
            packList: item.packList || [],
            promoList: item.promoList || []
        };
    });

    console.log("Loaded sealed products:", products);

    // Display lastUpdated timestamp
    if (data.length > 0 && data[0].lastUpdated) {
        const timestamp = data[0].lastUpdated;
        let date;
        
        // Check if it's a Firebase Timestamp object
        if (timestamp.toDate) {
            date = timestamp.toDate();
        } else if (timestamp.seconds) {
            // If it's a plain object with seconds
            date = new Date(timestamp.seconds * 1000);
        } else {
            date = new Date(timestamp);
        }
        
        // Convert to EST (UTC-5)
        const estOptions = {
            timeZone: 'America/New_York',
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZoneName: 'short'
        };
        
        const lastUpdatedText = date.toLocaleString('en-US', estOptions);
        
        document.getElementById("lastUpdated").textContent = `Last Updated: ${lastUpdatedText}`;
    } else {
        document.getElementById("lastUpdated").textContent = `Last Updated: N/A`;
    }

    // Apply the default filter
    applyFilter();
}

function handleError(error) {
    console.error("Error fetching data:", error);
    document.getElementById("products-list").innerHTML = "<li>Error loading products</li>";
}

// Function to display the list of products
function displayProducts() {
    const ul = document.getElementById("products-list");
    ul.innerHTML = ""; // Clear the existing list

    if (filteredProducts.length === 0) {
        ul.innerHTML = "<li>No products found</li>";
        return;
    }

    filteredProducts.forEach((product, productIndex) => {
        const li = document.createElement("li");
        li.className = "product-item";
        
        // Extract year from releaseDate
        let displayName = product.name;
        if (product.releaseDate) {
            const year = new Date(product.releaseDate).getFullYear();
            displayName = `${product.name} (${year})`;
        }
        
        // Create main product info (clickable)
        const productHeader = document.createElement("div");
        productHeader.className = "product-header";
        productHeader.setAttribute("data-product-index", productIndex);
        
        const profitSign = product.percentProfit >= 0 ? '+' : '';
        productHeader.textContent = `${displayName} - Price: $${product.price.toFixed(2)}, Total Value: $${product.totalValue.toFixed(2)}, Profit: ${profitSign}${product.percentProfit.toFixed(2)}%`;
        
        // Create expandable details section
        const detailsSection = document.createElement("div");
        detailsSection.className = "product-details";
        detailsSection.setAttribute("data-product-index", productIndex);
        detailsSection.style.display = "none";
        
        // Buy indicator
        const percentReturn = (product.totalValue / product.price) * 100;
        let buyIndicator = "";
        let buyClass = "";
        
        if (percentReturn >= 150) {
            buyIndicator = "Extreme Buy Or Likely Error";
            buyClass = "extreme-buy";
        } else if (percentReturn >= 120) {
            buyIndicator = "Strong Buy";
            buyClass = "strong-buy";
        } else if (percentReturn >= 100) {
            buyIndicator = "Moderate Buy";
            buyClass = "moderate-buy";
        } else if (percentReturn >= 80) {
            buyIndicator = "Ok Buy";
            buyClass = "ok-buy";
        } else if (percentReturn >= 60){
            buyIndicator = "Weak Buy";
            buyClass = "weak-buy";
        } else {
            buyIndicator = "Terrible Buy";
            buyClass = "terrible-buy";
        }
        
        
        const buyIndicatorDiv = document.createElement("div");
        buyIndicatorDiv.className = `buy-indicator ${buyClass}`;
        buyIndicatorDiv.textContent = `Buy Indicator: ${buyIndicator}`;
        detailsSection.appendChild(buyIndicatorDiv);
        
        // Value breakdown
        const valueBreakdown = document.createElement("div");
        valueBreakdown.className = "value-breakdown";
        valueBreakdown.style.marginTop = "15px";

        // Top row - Total values (centered)
        const totalsContainer = document.createElement("div");
        totalsContainer.style.display = "flex";
        totalsContainer.style.justifyContent = "center";
        totalsContainer.style.gap = "40px";
        totalsContainer.style.marginBottom = "20px";

        const promoValueDiv = document.createElement("div");
        promoValueDiv.innerHTML = `<strong>Total Promo Value:</strong> $${product.promoPrice.toFixed(2)}`;
        promoValueDiv.style.fontSize = "1.1rem";  // Add this line
        totalsContainer.appendChild(promoValueDiv);

        const packValueDiv = document.createElement("div");
        packValueDiv.innerHTML = `<strong>Total Pack Value:</strong> $${product.packTotal.toFixed(2)}`;
        packValueDiv.style.fontSize = "1.1rem";  // Add this line
        totalsContainer.appendChild(packValueDiv);

        valueBreakdown.appendChild(totalsContainer);

        // Bottom row - Lists (left: promos, right: packs)
        const listsContainer = document.createElement("div");
        listsContainer.style.display = "flex";
        listsContainer.style.justifyContent = "space-between";
        listsContainer.style.gap = "20px";

        // Left side - promo list
        const promoContainer = document.createElement("div");
        if (product.promoList && product.promoList.length > 0) {
            const promoListTitle = document.createElement("div");
            promoListTitle.innerHTML = `<strong>Promos Included:</strong>`;
            promoListTitle.style.marginBottom = "5px";
            promoContainer.appendChild(promoListTitle);
            
            product.promoList.forEach((promo) => {
                const promoItem = document.createElement("div");
                promoItem.textContent = `${promo.name} - $${promo.price.toFixed(2)}`;
                promoItem.style.padding = "2px 0";
                promoContainer.appendChild(promoItem);
            });
        }
        listsContainer.appendChild(promoContainer);

        // Right side - pack list
        const packContainer = document.createElement("div");
        if (product.packList && product.packList.length > 0) {
            const packListTitle = document.createElement("div");
            packListTitle.innerHTML = `<strong>Packs Included:</strong>`;
            packListTitle.style.marginBottom = "5px";
            packContainer.appendChild(packListTitle);
            
            product.packList.forEach((pack) => {
                const packItem = document.createElement("div");
                packItem.textContent = `(${pack.count}x) ${pack.name} - $${pack.price.toFixed(2)}`;
                packItem.style.padding = "2px 0";
                packContainer.appendChild(packItem);
            });
        }
        listsContainer.appendChild(packContainer);

        valueBreakdown.appendChild(listsContainer);
        detailsSection.appendChild(valueBreakdown);
        
        li.appendChild(productHeader);
        li.appendChild(detailsSection);
        ul.appendChild(li);
    });
    
    // Use event delegation
    ul.addEventListener("click", handleProductListClick);
    
    console.log("Finished displaying products");
}

// Event delegation handler
function handleProductListClick(event) {
    const target = event.target;
    
    // Handle product header clicks
    if (target.classList.contains("product-header")) {
        const productIndex = parseInt(target.getAttribute("data-product-index"));
        const detailsSection = target.nextElementSibling;
        
        console.log("Product header clicked:", filteredProducts[productIndex].name);
        
        const isExpanded = detailsSection.style.display === "block";
        detailsSection.style.display = isExpanded ? "none" : "block";
        target.classList.toggle("expanded", !isExpanded);
    }
    
    // Handle close button clicks
    if (target.classList.contains("close-details-btn")) {
        event.stopPropagation();
        const productIndex = parseInt(target.getAttribute("data-product-index"));
        const detailsSection = target.parentElement;
        const productHeader = detailsSection.previousElementSibling;
        
        console.log("Close button clicked");
        
        detailsSection.style.display = "none";
        productHeader.classList.remove("expanded");
    }
}

// Function to handle sorting based on selected criteria
function sortProducts(criteria) {
    const sorters = {
        nameAsc: (a, b) => a.name.localeCompare(b.name),
        nameDesc: (a, b) => b.name.localeCompare(a.name),
        priceAsc: (a, b) => a.price - b.price,
        priceDesc: (a, b) => b.price - a.price,
        valueAsc: (a, b) => a.totalValue - b.totalValue,
        valueDesc: (a, b) => b.totalValue - a.totalValue,
        profitAsc: (a, b) => a.percentProfit - b.percentProfit,
        profitDesc: (a, b) => b.percentProfit - a.percentProfit,
        releaseAsc: (a, b) => {
            const dateA = new Date(a.releaseDate);
            const dateB = new Date(b.releaseDate);
            return dateB - dateA; // Latest to Earliest
        },
        releaseDesc: (a, b) => {
            const dateA = new Date(a.releaseDate);
            const dateB = new Date(b.releaseDate);
            return dateA - dateB; // Earliest to Latest
        },
    };

    if (sorters[criteria]) {
        lastSortCriteria = criteria;
        filteredProducts.sort(sorters[criteria]);
        
        // Remove old event listener before re-rendering
        const ul = document.getElementById("products-list");
        ul.removeEventListener("click", handleProductListClick);
        
        displayProducts();
    } else {
        console.error("Invalid sort criteria:", criteria);
    }
}

// Function to filter products based on the selected criteria
function applyFilter() {
    const filterers = {
        all: () => products,
        // Add more filters here as needed
    };

    if (filterers[activeFilter]) {
        filteredProducts = filterers[activeFilter]();
        console.log("Filtered Products:", filteredProducts);
        sortProducts(lastSortCriteria);
    } else {
        console.error("Invalid filter criteria:", activeFilter);
    }
}

// Event listener for sorting dropdown
const sortDropdown = document.getElementById("sortDropdown");
if (sortDropdown) {
    sortDropdown.addEventListener("change", (event) => {
        const sortCriteria = event.target.value;
        sortProducts(sortCriteria);
    });
}

// Event listener for filtering dropdown
const filterDropdown = document.getElementById("filterDropdown");
if (filterDropdown) {
    filterDropdown.addEventListener("change", (event) => {
        activeFilter = event.target.value;
        console.log("New Active Filter:", activeFilter);
        applyFilter();
    });
}

// Calculate Sealed Product Value
document.querySelector(".productValueButton").addEventListener("click", async function () {
    // Fetch packs data if not already loaded
    if (!window.packsData) {
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        window.packsData = [];
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            window.packsData.push({
                name: data.setName,
                value: data.packValue,
                ev: data.ev,
                adjustedEv: data.adjustedEv
            });
        });
    }

    const productPrice = parseFloat(prompt("Enter the price of the product:"));
    if (isNaN(productPrice)) {
        alert("Invalid price entered. Please enter a numeric value.");
        return;
    }
    const negativeProductPrice = -Math.abs(productPrice);

    const numberOfPacks = parseInt(prompt("Enter the number of packs in the product:"), 10);
    if (isNaN(numberOfPacks) || numberOfPacks <= 0) {
        alert("Please enter a valid number of packs!");
        return;
    }

    let packTotal = 0;
    for (let i = 0; i < numberOfPacks; i++) {
        const packName = prompt(`Enter the name of pack ${i + 1}:`);
        const pack = window.packsData.find((p) => p.name.toLowerCase() === packName.toLowerCase());

        if (pack) {
            packTotal += parseFloat(pack.value);
            alert(`Pack '${pack.name}' with value of $${pack.value} added. Running total: $${packTotal.toFixed(2)}`);
        } else {
            alert(`Pack '${packName}' not found. Skipping.`);
        }
    }

    const totalProfit = packTotal + negativeProductPrice;
    const percentProfit = ((packTotal / Math.abs(negativeProductPrice)) - 1) * 100;

    alert(`Total Value of packs: $${packTotal.toFixed(2)}\n` + 
          `Total Profit: $${totalProfit.toFixed(2)}\n` + 
          `Percent Profit: ${percentProfit.toFixed(2)}%`);
});

// Calculate EV for a Sealed Product
document.querySelector(".sealedProductEvButton").addEventListener("click", async function () {
    // Fetch packs data if not already loaded
    if (!window.packsData) {
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        window.packsData = [];
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            window.packsData.push({
                name: data.setName,
                value: data.packValue,
                ev: data.ev,
                adjustedEv: data.adjustedEv
            });
        });
    }

    const productPrice = parseFloat(prompt("Enter the price of the sealed product:"));
    if (isNaN(productPrice)) {
        alert("Invalid price entered. Please enter a numeric value.");
        return;
    }
    const negativeProductPrice = -Math.abs(productPrice);

    const numberOfPacks = parseInt(prompt("Enter the number of packs in the sealed product:"), 10);
    if (isNaN(numberOfPacks) || numberOfPacks <= 0) {
        alert("Please enter a valid number of packs!");
        return;
    }

    let packTotalEv = 0;
    for (let i = 0; i < numberOfPacks; i++) {
        const packName = prompt(`Enter the name of pack ${i + 1}:`);
        const pack = window.packsData.find((p) => p.name.toLowerCase() === packName.toLowerCase());

        if (pack) {
            packTotalEv += parseFloat(pack.ev);
            alert(`Pack '${pack.name}' with EV of $${pack.ev} added. Running total EV: $${packTotalEv.toFixed(2)}`);
        } else {
            alert(`Pack '${packName}' not found. Skipping.`);
        }
    }

    const sealedProductEv = packTotalEv + negativeProductPrice;

    alert(`Total EV of packs: $${packTotalEv.toFixed(2)}\n` +
          `Expected Profit for the sealed product: $${sealedProductEv.toFixed(2)}`);
});

// Calculate EV for Multiple Packs
document.querySelector(".multiplePacksEvButton").addEventListener("click", async function () {
    // Fetch packs data if not already loaded
    if (!window.packsData) {
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        window.packsData = [];
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            window.packsData.push({
                name: data.setName,
                value: data.packValue,
                ev: data.ev,
                adjustedEv: data.adjustedEv
            });
        });
    }

    let totalEv = 0;

    while (true) {
        const packName = prompt("Enter the pack name (or type 'done' to finish):").trim();
        if (packName.toLowerCase() === "done") break;

        const pack = window.packsData.find((p) => p.name.toLowerCase() === packName.toLowerCase());

        if (pack) {
            totalEv += parseFloat(pack.ev);
            alert(`Pack '${pack.name}' with EV of $${pack.ev} added. Running total EV: $${totalEv.toFixed(2)}`);
        } else {
            alert(`Pack '${packName}' not found. Please try again.`);
        }
    }

    alert(`Total EV for the entered packs: $${totalEv.toFixed(2)}`);
});

// Calculate EV for a Single Pack
document.querySelector(".singlePackEvButton").addEventListener("click", async function () {
    // Fetch packs data if not already loaded
    if (!window.packsData) {
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        window.packsData = [];
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            window.packsData.push({
                name: data.setName,
                value: data.packValue,
                ev: data.ev,
                adjustedEv: data.adjustedEv
            });
        });
    }

    const packName = prompt("Enter the name of the pack:").trim();
    const pack = window.packsData.find((p) => p.name.toLowerCase() === packName.toLowerCase());

    if (pack) {
        const totalEv = parseFloat(pack.ev);
        alert(`Pack: ${pack.name}\nEV: $${totalEv.toFixed(2)}\nReturn on Investment: ${(pack.adjustedEv * 100).toFixed(2)}%`);
    } else {
        alert(`Pack '${packName}' not found.`);
    }
});

// Fetch sealed products
fetchProducts();