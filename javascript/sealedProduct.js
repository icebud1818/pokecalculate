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
        const percentProfit = item.price > 0 ? ((item.packTotal - item.price) / item.price) * 100 : 0;
        
        return {
            id: item.id,
            productId: item.productId,
            name: item.name,
            price: item.price,
            promoPrice: item.promoPrice,
            packTotal: item.packTotal,
            percentProfit: percentProfit,
            packs: item.packs || [],
            promos: item.promos || []
        };
    });

    console.log("Loaded sealed products:", products);

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

    filteredProducts.forEach((product) => {
        const li = document.createElement("li");
        const profitSign = product.percentProfit >= 0 ? '+' : '';
        li.textContent = `${product.name} - Price: ${product.price.toFixed(2)}, Pack Value: ${product.packTotal.toFixed(2)}, Profit: ${profitSign}${product.percentProfit.toFixed(2)}%`;
        ul.appendChild(li);
    });
}

// Function to handle sorting based on selected criteria
function sortProducts(criteria) {
    const sorters = {
        nameAsc: (a, b) => a.name.localeCompare(b.name),
        nameDesc: (a, b) => b.name.localeCompare(a.name),
        priceAsc: (a, b) => a.price - b.price,
        priceDesc: (a, b) => b.price - a.price,
        valueAsc: (a, b) => a.packTotal - b.packTotal,
        valueDesc: (a, b) => b.packTotal - a.packTotal,
        profitAsc: (a, b) => a.percentProfit - b.percentProfit,
        profitDesc: (a, b) => b.percentProfit - a.percentProfit,
    };

    if (sorters[criteria]) {
        lastSortCriteria = criteria;
        filteredProducts.sort(sorters[criteria]);
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

// Fetch sealed products
fetchProducts();