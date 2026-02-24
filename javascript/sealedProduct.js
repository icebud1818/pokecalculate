let products = [];
let filteredProducts = [];
let lastSortCriteria = "nameAsc";
let eventListenerAttached = false;

// Active filters state
let activeFilters = {
    yearFrom:         null,
    yearTo:           null,
    priceMin:         null,
    priceMax:         null,
    buyIndicatorFrom: "terrible-buy",
    buyIndicatorTo:   "extreme-buy"
};

// Helper: get buy indicator class for a product
function getBuyIndicatorClass(product) {
    const percentReturn = (product.totalValue / product.price) * 100;
    if (percentReturn >= 150) return "extreme-buy";
    if (percentReturn >= 120) return "strong-buy";
    if (percentReturn >= 100) return "moderate-buy";
    if (percentReturn >= 80)  return "ok-buy";
    if (percentReturn >= 60)  return "weak-buy";
    return "terrible-buy";
}

// Helper: get buy indicator label for a product
function getBuyIndicatorLabel(buyClass) {
    const labels = {
        "extreme-buy":  "Extreme Buy Or Likely Error",
        "strong-buy":   "Strong Buy",
        "moderate-buy": "Moderate Buy",
        "ok-buy":       "Ok Buy",
        "weak-buy":     "Weak Buy",
        "terrible-buy": "Terrible Buy"
    };
    return labels[buyClass] || "";
}

// Lower number = better rating
const BUY_INDICATOR_RANK = {
    "extreme-buy":  0,
    "strong-buy":   1,
    "moderate-buy": 2,
    "ok-buy":       3,
    "weak-buy":     4,
    "terrible-buy": 5
};

// Helper: calculate total EV for a product (pack EVs * count + promo value)
function calculateProductEV(product) {
    if (!window.packsData || !product.packList) return null;

    let packEVTotal = 0;
    for (const pack of product.packList) {
        const match = window.packsData.find(
            (p) => p.name.toLowerCase() === pack.name.toLowerCase()
        );
        if (match) {
            packEVTotal += match.ev * pack.count;
        }
    }

    return packEVTotal + product.promoPrice;
}

// Fetch sealed products data from Firebase Firestore
async function fetchProducts() {
    console.log("Starting to fetch sealed products...");
    
    try {
        let attempts = 0;
        while (!window.db || !window.collection || !window.getDocs) {
            console.log("Waiting for Firebase to initialize...", attempts);
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
            if (attempts > 50) throw new Error("Firebase failed to initialize after 5 seconds");
        }

        console.log("Firebase initialized, fetching sealedProducts collection...");
        const querySnapshot = await window.getDocs(window.collection(window.db, "sealedProducts"));
        console.log("Sealed products query snapshot received, size:", querySnapshot.size);
        
        const data = [];
        querySnapshot.forEach((doc) => {
            data.push({ id: doc.id, ...doc.data() });
        });

        console.log("Total sealed products fetched:", data.length);
        await initializeProducts(data);
    } catch (error) {
        handleError(error);
    }
}

async function initializeProducts(data) {
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

    if (data.length > 0 && data[0].lastUpdated) {
        const timestamp = data[0].lastUpdated;
        let date;
        if (timestamp.toDate) {
            date = timestamp.toDate();
        } else if (timestamp.seconds) {
            date = new Date(timestamp.seconds * 1000);
        } else {
            date = new Date(timestamp);
        }
        
        const estOptions = {
            timeZone: 'America/New_York',
            weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short'
        };
        document.getElementById("lastUpdated").textContent = `Last Updated: ${date.toLocaleString('en-US', estOptions)}`;
    } else {
        document.getElementById("lastUpdated").textContent = `Last Updated: N/A`;
    }

    // Load pack EV data so calculateProductEV works when user expands a product
    await ensurePacksData();

    attachEventListener();
    applyFilter();
}

function handleError(error) {
    console.error("Error fetching data:", error);
    document.getElementById("products-list").innerHTML = "<li>Error loading products</li>";
}

function attachEventListener() {
    if (!eventListenerAttached) {
        const ul = document.getElementById("products-list");
        ul.addEventListener("click", handleProductListClick);
        eventListenerAttached = true;
    }
}

function displayProducts() {
    const ul = document.getElementById("products-list");
    ul.innerHTML = "";

    if (filteredProducts.length === 0) {
        ul.innerHTML = "<li>No products found</li>";
        return;
    }

    filteredProducts.forEach((product, productIndex) => {
        const li = document.createElement("li");
        li.className = "product-item";
        
        let displayName = product.name;
        if (product.releaseDate) {
            const year = new Date(product.releaseDate).getFullYear();
            displayName = `${product.name} (${year})`;
        }
        
        const productHeader = document.createElement("div");
        productHeader.className = "product-header";
        productHeader.setAttribute("data-product-index", productIndex);
        
        const profitSign = product.percentProfit >= 0 ? '+' : '';
        productHeader.textContent = `${displayName} - Price: $${product.price.toFixed(2)}, Total Value: $${product.totalValue.toFixed(2)}, Profit: ${profitSign}${product.percentProfit.toFixed(2)}%`;
        
        const detailsSection = document.createElement("div");
        detailsSection.className = "product-details";
        detailsSection.setAttribute("data-product-index", productIndex);
        detailsSection.style.display = "none";
        
        // Buy indicator
        const buyClass = getBuyIndicatorClass(product);
        const buyIndicatorDiv = document.createElement("div");
        buyIndicatorDiv.className = `buy-indicator ${buyClass}`;
        buyIndicatorDiv.textContent = `Buy Indicator: ${getBuyIndicatorLabel(buyClass)}`;
        detailsSection.appendChild(buyIndicatorDiv);
        
        // Value breakdown
        const valueBreakdown = document.createElement("div");
        valueBreakdown.className = "value-breakdown";
        valueBreakdown.style.marginTop = "15px";

        const totalsContainer = document.createElement("div");
        totalsContainer.style.cssText = "display:flex; justify-content:center; gap:20px; margin-bottom:20px; align-items:center; text-align:center;";

        const promoValueDiv = document.createElement("div");
        promoValueDiv.innerHTML = `<strong>Total Promo Value:</strong> $${product.promoPrice.toFixed(2)}`;
        promoValueDiv.style.fontSize = "font-size:1.1rem; text-align:center;";
        totalsContainer.appendChild(promoValueDiv);

        const totalEV = calculateProductEV(product);
        const evDiv = document.createElement("div");
        evDiv.innerHTML = `<strong>Total Expected Value:</strong> ${totalEV !== null ? '$' + totalEV.toFixed(2) : 'N/A'}`;
        evDiv.style.fontSize = "font-size:1.1rem; text-align:center;";
        totalsContainer.appendChild(evDiv);

        const packValueDiv = document.createElement("div");
        packValueDiv.innerHTML = `<strong>Total Pack Value:</strong> $${product.packTotal.toFixed(2)}`;
        packValueDiv.style.fontSize = "font-size:1.1rem; text-align:center;";
        totalsContainer.appendChild(packValueDiv);

        valueBreakdown.appendChild(totalsContainer);

        const listsContainer = document.createElement("div");
        listsContainer.style.cssText = "display:flex; justify-content:space-between; gap:20px;";

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
    
    console.log("Finished displaying products");
}

function handleProductListClick(event) {
    const target = event.target;
    
    if (target.classList.contains("product-header")) {
        const detailsSection = target.nextElementSibling;
        const isExpanded = detailsSection.style.display === "block";
        detailsSection.style.display = isExpanded ? "none" : "block";
        target.classList.toggle("expanded", !isExpanded);
    }
    
    if (target.classList.contains("close-details-btn")) {
        event.stopPropagation();
        const detailsSection = target.parentElement;
        const productHeader = detailsSection.previousElementSibling;
        detailsSection.style.display = "none";
        productHeader.classList.remove("expanded");
    }
}

function sortProducts(criteria) {
    const sorters = {
        nameAsc:     (a, b) => a.name.localeCompare(b.name),
        nameDesc:    (a, b) => b.name.localeCompare(a.name),
        priceAsc:    (a, b) => a.price - b.price,
        priceDesc:   (a, b) => b.price - a.price,
        valueAsc:    (a, b) => a.totalValue - b.totalValue,
        valueDesc:   (a, b) => b.totalValue - a.totalValue,
        profitAsc:   (a, b) => a.percentProfit - b.percentProfit,
        profitDesc:  (a, b) => b.percentProfit - a.percentProfit,
        releaseAsc:  (a, b) => new Date(b.releaseDate) - new Date(a.releaseDate),
        releaseDesc: (a, b) => new Date(a.releaseDate) - new Date(b.releaseDate),
    };

    if (sorters[criteria]) {
        lastSortCriteria = criteria;
        filteredProducts.sort(sorters[criteria]);
        displayProducts();
    } else {
        console.error("Invalid sort criteria:", criteria);
    }
}

function applyFilter() {
    filteredProducts = products.filter((product) => {
        // --- Year range filter ---
        if (activeFilters.yearFrom !== null || activeFilters.yearTo !== null) {
            if (!product.releaseDate) return false;
            const year = new Date(product.releaseDate).getFullYear();
            if (activeFilters.yearFrom !== null && year < activeFilters.yearFrom) return false;
            if (activeFilters.yearTo   !== null && year > activeFilters.yearTo)   return false;
        }

        // --- Price range filter ---
        if (activeFilters.priceMin !== null && product.price < activeFilters.priceMin) return false;
        if (activeFilters.priceMax !== null && product.price > activeFilters.priceMax) return false;

        // --- Buy indicator range filter ---
        const productRank = BUY_INDICATOR_RANK[getBuyIndicatorClass(product)];
        const fromRank    = BUY_INDICATOR_RANK[activeFilters.buyIndicatorFrom];
        const toRank      = BUY_INDICATOR_RANK[activeFilters.buyIndicatorTo];
        const minRank     = Math.min(fromRank, toRank);
        const maxRank     = Math.max(fromRank, toRank);
        if (productRank < minRank || productRank > maxRank) return false;

        return true;
    });

    console.log("Filtered products:", filteredProducts.length);
    sortProducts(lastSortCriteria);
}

// --- Filter button listeners ---
document.getElementById("applyFiltersBtn").addEventListener("click", () => {
    const yearFrom = document.getElementById("yearFrom").value;
    const yearTo   = document.getElementById("yearTo").value;
    const priceMin = document.getElementById("priceMin").value;
    const priceMax = document.getElementById("priceMax").value;

    activeFilters.yearFrom         = yearFrom ? parseInt(yearFrom)   : null;
    activeFilters.yearTo           = yearTo   ? parseInt(yearTo)     : null;
    activeFilters.priceMin         = priceMin ? parseFloat(priceMin) : null;
    activeFilters.priceMax         = priceMax ? parseFloat(priceMax) : null;
    activeFilters.buyIndicatorFrom = document.getElementById("buyIndicatorFrom").value;
    activeFilters.buyIndicatorTo   = document.getElementById("buyIndicatorTo").value;

    applyFilter();
});

document.getElementById("clearFiltersBtn").addEventListener("click", () => {
    activeFilters = {
        yearFrom:         null,
        yearTo:           null,
        priceMin:         null,
        priceMax:         null,
        buyIndicatorFrom: "terrible-buy",
        buyIndicatorTo:   "extreme-buy"
    };

    document.getElementById("yearFrom").value         = "";
    document.getElementById("yearTo").value           = "";
    document.getElementById("priceMin").value         = "";
    document.getElementById("priceMax").value         = "";
    document.getElementById("buyIndicatorFrom").value = "terrible-buy";
    document.getElementById("buyIndicatorTo").value   = "extreme-buy";

    applyFilter();
});

// --- Sort dropdown ---
const sortDropdown = document.getElementById("sortDropdown");
if (sortDropdown) {
    sortDropdown.addEventListener("change", (event) => {
        sortProducts(event.target.value);
    });
}

// --- Calculator buttons ---
async function ensurePacksData() {
    if (!window.packsData) {
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        window.packsData = [];
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            window.packsData.push({
                name: data.setName, value: data.packValue,
                ev: data.ev, adjustedEv: data.adjustedEv
            });
        });
    }
}

const productValueButton = document.querySelector(".productValueButton");
if (productValueButton) {
    productValueButton.addEventListener("click", async function () {
        await ensurePacksData();
        const productPrice = parseFloat(prompt("Enter the price of the product:"));
        if (isNaN(productPrice)) { alert("Invalid price entered."); return; }
        const negativeProductPrice = -Math.abs(productPrice);
        const numberOfPacks = parseInt(prompt("Enter the number of packs in the product:"), 10);
        if (isNaN(numberOfPacks) || numberOfPacks <= 0) { alert("Please enter a valid number of packs!"); return; }

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
        alert(`Total Value of packs: $${packTotal.toFixed(2)}\nTotal Profit: $${totalProfit.toFixed(2)}\nPercent Profit: ${percentProfit.toFixed(2)}%`);
    });
}

const sealedProductEvButton = document.querySelector(".sealedProductEvButton");
if (sealedProductEvButton) {
    sealedProductEvButton.addEventListener("click", async function () {
        await ensurePacksData();
        const productPrice = parseFloat(prompt("Enter the price of the sealed product:"));
        if (isNaN(productPrice)) { alert("Invalid price entered."); return; }
        const negativeProductPrice = -Math.abs(productPrice);
        const numberOfPacks = parseInt(prompt("Enter the number of packs in the sealed product:"), 10);
        if (isNaN(numberOfPacks) || numberOfPacks <= 0) { alert("Please enter a valid number of packs!"); return; }

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
        alert(`Total EV of packs: $${packTotalEv.toFixed(2)}\nExpected Profit: $${(packTotalEv + negativeProductPrice).toFixed(2)}`);
    });
}

const multiplePacksEvButton = document.querySelector(".multiplePacksEvButton");
if (multiplePacksEvButton) {
    multiplePacksEvButton.addEventListener("click", async function () {
        await ensurePacksData();
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
}

const singlePackEvButton = document.querySelector(".singlePackEvButton");
if (singlePackEvButton) {
    singlePackEvButton.addEventListener("click", async function () {
        await ensurePacksData();
        const packName = prompt("Enter the name of the pack:").trim();
        const pack = window.packsData.find((p) => p.name.toLowerCase() === packName.toLowerCase());
        if (pack) {
            alert(`Pack: ${pack.name}\nEV: $${parseFloat(pack.ev).toFixed(2)}\nReturn on Investment: ${(pack.adjustedEv * 100).toFixed(2)}%`);
        } else {
            alert(`Pack '${packName}' not found.`);
        }
    });
}

fetchProducts();