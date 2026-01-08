let products = [];
let sets = [];
let filteredProducts = [];
let activeFilter = "all";
let lastSortCriteria = "nameAsc";

// Fetch sets data from Firebase Firestore
async function fetchSets() {
    console.log("Starting to fetch sets...");
    
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

        console.log("Firebase initialized, fetching sets collection...");
        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        console.log("Sets query snapshot received, size:", querySnapshot.size);
        
        const data = [];
        
        querySnapshot.forEach((doc) => {
            console.log("Set document data:", doc.id, doc.data());
            data.push({
                id: doc.id,
                ...doc.data()
            });
        });

        console.log("Total sets fetched:", data.length);
        sets = data;
        
        // After sets are loaded, fetch products
        fetchProducts();
    } catch (error) {
        handleError(error);
    }
}

// Fetch products data from Firebase Firestore
async function fetchProducts() {
    console.log("Starting to fetch products...");
    
    try {
        console.log("Fetching products collection...");
        const querySnapshot = await window.getDocs(window.collection(window.db, "products"));
        console.log("Products query snapshot received, size:", querySnapshot.size);
        
        const data = [];
        
        querySnapshot.forEach((doc) => {
            console.log("Product document data:", doc.id, doc.data());
            data.push({
                id: doc.id,
                ...doc.data()
            });
        });

        console.log("Total products fetched:", data.length);
        initializeProducts(data);
    } catch (error) {
        handleError(error);
    }
}

// Calculate the total value of packs in a product
function calculatePackValue(packsArray) {
    let totalValue = 0;
    
    console.log("Calculating pack value for:", packsArray);
    console.log("Available sets:", sets);
    
    if (!packsArray || packsArray.length === 0) {
        console.log("No packs array found");
        return 0;
    }
    
    // Iterate through each pack map in the array
    packsArray.forEach((packMap) => {
        console.log("Processing pack map:", packMap);
        
        // Each packMap is an object like { "901.5": 4 }
        Object.keys(packMap).forEach((setNumber) => {
            const quantity = packMap[setNumber];
            console.log(`Looking for setNumber: ${setNumber} (type: ${typeof setNumber}), quantity: ${quantity}`);
            
            // Find the matching set by setNumber
            const matchingSet = sets.find((set) => {
                console.log(`Comparing with set.setNumber: ${set.setNumber} (type: ${typeof set.setNumber})`);
                return String(set.setNumber) === String(setNumber);
            });
            
            if (matchingSet && matchingSet.packValue) {
                const packPrice = matchingSet.packValue;
                const value = packPrice * quantity;
                console.log(`✓ MATCH FOUND! Set ${setNumber}: ${packPrice} x ${quantity} = ${value}`);
                totalValue += value;
            } else {
                console.warn(`✗ No matching set found for setNumber: ${setNumber}`);
                if (matchingSet) {
                    console.warn("Set found but no packValue:", matchingSet);
                }
            }
        });
    });
    
    console.log("Total pack value:", totalValue);
    return totalValue;
}

function initializeProducts(data) {
    products = data.map((item) => {
        const packValue = calculatePackValue(item.packs);
        const percentProfit = item.price > 0 ? ((packValue - item.price) / item.price) * 100 : 0;
        
        return {
            id: item.id,
            name: item.name,
            price: item.price,
            packs: item.packs || [],
            packValue: packValue,
            percentProfit: percentProfit
        };
    });

    console.log("Loaded products:", products);

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
        li.textContent = `${product.name} - Price: ${product.price.toFixed(2)}, Pack Value: ${product.packValue.toFixed(2)}, Profit: ${profitSign}${product.percentProfit.toFixed(2)}%`;
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
        valueAsc: (a, b) => a.packValue - b.packValue,
        valueDesc: (a, b) => b.packValue - a.packValue,
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
        // Add more filters here as needed based on generation
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

// Fetch sets first, then products
fetchSets();