let boxes = [];
let packs = [];
let filteredBoxes = [];
let filteredPacks = [];
let activeFilter = "all";
let lastSortCriteria = "nameAsc";

// Fetch boxes data from Firebase Firestore
async function fetchBoxes() {
    try {
        // Wait for Firebase to be initialized
        while (!window.db || !window.collection || !window.getDocs) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        const querySnapshot = await window.getDocs(window.collection(window.db, "boosterBoxes"));
        const data = [];
        
        querySnapshot.forEach((doc) => {
            data.push(doc.data());
        });

        initializeBoxes(data);
    } catch (error) {
        handleError(error);
    }
}

// Fetch packs data from Firebase Firestore
async function fetchPacks() {
    try {
        // Wait for Firebase to be initialized
        while (!window.db || !window.collection || !window.getDocs) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        const querySnapshot = await window.getDocs(window.collection(window.db, "sets"));
        const data = [];
        
        querySnapshot.forEach((doc) => {
            data.push(doc.data());
        });

        initializePacks(data);
    } catch (error) {
        handleError(error);
    }
}

function initializePacks(data) {
    packs = data.map((item) => ({
        name: item.setName,
        value: item.packValue,
        ev: item.ev,
        adjEv: item.adjustedEv,
        setNumber: parseInt(item.setNumber, 10),
    }));

    // Apply the default filter
    applyFilter();
    
    // After packs are loaded, fetch boxes
    fetchBoxes();
}

function initializeBoxes(data) {
    boxes = data.map((item) => {
        const matchingPack = packs.find((pack) => pack.setNumber === parseInt(item.setNumber, 10));
        const ev = matchingPack ? matchingPack.ev * 36 : null; // EV for the entire box
        const value = item.boxPrice;
        const pricePer = item.pricePer;
        const loosePrice = matchingPack ? matchingPack.value : null; // Get loose price from the matching pack
        const percentReturn = ev && value ? (ev / value) * 100 : null; // Calculate percent return if ev and value are valid
        const boxPremium = loosePrice && pricePer ? ((pricePer / loosePrice) - 1) * 100 : null; // Calculate box premium if both loosePrice and pricePer are valid
    
        return {
            name: item.setName,
            value: value,
            pricePer: pricePer,
            setNumber: parseInt(item.setNumber, 10),
            ev: ev,
            percentReturn: percentReturn,
            boxPremium: boxPremium,
        };
    });

    // Get the most recent lastUpdated timestamp
    if (data.length > 0 && data[0].lastUpdated) {
        const timestamp = data[0].lastUpdated;
        let lastUpdatedText;
        
        // Check if it's a Firebase Timestamp object
        if (timestamp.toDate) {
            lastUpdatedText = timestamp.toDate().toUTCString();
        } else if (timestamp.seconds) {
            // If it's a plain object with seconds
            lastUpdatedText = new Date(timestamp.seconds * 1000).toUTCString();
        } else {
            lastUpdatedText = timestamp;
        }
        
        document.getElementById("lastUpdated").textContent = `Last Updated: ${lastUpdatedText}`;
    } else {
        document.getElementById("lastUpdated").textContent = `Last Updated: N/A`;
    }

    applyBoxFilter(); // Apply the default filter
}

function handleError(error) {
    console.error("Error fetching pack data:", error);
    document.getElementById("packs-list").innerHTML = "<li>Error loading packs</li>";
}

// Function to display the list of boxes
function displayPacks() {
    const ul = document.getElementById("packs-list");
    ul.innerHTML = ""; // Clear the existing list

    filteredBoxes.forEach((box) => {
        const li = document.createElement("li");
        li.textContent = `${box.name} - Box Price: $${box.value.toFixed(2)}, EV: $${box.ev.toFixed(2)}, Percent Return: ${box.percentReturn.toFixed(2)}%, Price Per Pack: $${box.pricePer.toFixed(
            2
        )}, Box Premium: ${box.boxPremium.toFixed(2)}%`;
        ul.appendChild(li);
    });
}

// Function to handle sorting based on selected criteria
function sortPacks(criteria) {
    const sorters = {
        nameAsc: (a, b) => a.name.localeCompare(b.name),
        nameDesc: (a, b) => b.name.localeCompare(a.name),
        valueAsc: (a, b) => a.pricePer - b.pricePer,
        valueDesc: (a, b) => b.pricePer - a.pricePer,
        priceAsc: (a, b) => a.value - b.value,
        priceDesc: (a, b) => b.value - a.value,
        setNumberAsc: (a, b) => a.setNumber - b.setNumber,
        setNumberDesc: (a, b) => b.setNumber - a.setNumber,
        evAsc: (a, b) => a.ev - b.ev,
        evDesc: (a, b) => b.ev - a.ev,
        boxPremiumAsc: (a, b) => a.boxPremium - b.boxPremium,
        boxPremiumDesc: (a, b) => b.boxPremium - a.boxPremium,
        percentReturnAsc: (a, b) => a.percentReturn - b.percentReturn,
        percentReturnDesc: (a, b) => b.percentReturn - a.percentReturn,
    };

    if (sorters[criteria]) {
        lastSortCriteria = criteria; // Update the sorting criteria
        filteredBoxes.sort(sorters[criteria]); // Sort the currently filtered boxes
        displayPacks(); // Refresh the list
    } else {
        console.error("Invalid sort criteria:", criteria);
    }
}

// Function to filter boxes based on the selected criteria
function applyBoxFilter() {
    const filterers = {
        all: () => boxes,
        gen6: () => boxes.filter((box) => box.setNumber >= 800 && box.setNumber <= 811),
        gen7: () => boxes.filter((box) => box.setNumber >= 900 && box.setNumber <= 911),
        gen8: () => boxes.filter((box) => box.setNumber >= 1000 && box.setNumber <= 1103),
        gen9: () => boxes.filter((box) => box.setNumber >= 1200 && box.setNumber <= 1211),
    };

    if (filterers[activeFilter]) {
        filteredBoxes = filterers[activeFilter](); // Apply the selected filter
        console.log("Filtered Boxes:", filteredBoxes); // Debug filtered results
        sortPacks(lastSortCriteria); // Reapply the last sorting
    } else {
        console.error("Invalid filter criteria:", activeFilter);
    }
}

function applyFilter() {
    const filterers = {
        all: () => packs,
        gen1: () => packs.filter((pack) => pack.setNumber <= 106),
        gen2: () => packs.filter((pack) => pack.setNumber >= 107 && pack.setNumber <= 203),
        gen3: () => packs.filter((pack) => pack.setNumber >= 300 && pack.setNumber <= 408),
        gen4: () => packs.filter((pack) => pack.setNumber >= 500 && pack.setNumber <= 604),
        gen5: () => packs.filter((pack) => pack.setNumber >= 700 && pack.setNumber <= 710),
        gen6: () => packs.filter((pack) => pack.setNumber >= 800 && pack.setNumber <= 811),
        gen7: () => packs.filter((pack) => pack.setNumber >= 900 && pack.setNumber <= 911),
        gen8: () => packs.filter((pack) => pack.setNumber >= 1000 && pack.setNumber <= 1103),
        gen9: () => packs.filter((pack) => pack.setNumber >= 1200 && pack.setNumber <= 1211)
    };

    if (filterers[activeFilter]) {
        filteredPacks = filterers[activeFilter](); // Apply the selected filter
    } else {
        console.error("Invalid filter criteria:", activeFilter);
    }
}

// Event listener for sorting dropdown
document.getElementById("sortDropdown").addEventListener("change", (event) => {
    const sortCriteria = event.target.value;
    sortPacks(sortCriteria); // Sort the filtered list
});

// Event listener for filtering dropdown
document.getElementById("filterDropdown").addEventListener("change", (event) => {
    activeFilter = event.target.value; // Update the active filter
    console.log("New Active Filter:", activeFilter); // Debug active filter
    applyBoxFilter(); // Apply the new filter
});

// Fetch and initialize packs on page load (packs must load first, then boxes)
fetchPacks();

function findExactPack(packName) {
    return boxes.find((pack) => pack.name.toLowerCase() === packName.toLowerCase());
}