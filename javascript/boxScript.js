let boxes = [];
let packs = [];
let filteredBoxes = [];
let filteredPacks = [];
let activeFilter = "all";
let lastSortCriteria = "nameAsc";

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

        await initializePacks(data);
    } catch (error) {
        handleError(error);
    }
}

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

async function initializePacks(data) {
    packs = data.map((item) => ({
        name: item.setName,
        value: item.packValue,
        ev: item.ev,
        adjEv: item.adjustedEv,
        setNumber: parseFloat(item.setNumber),
    }));

    console.log("Packs loaded:", packs.length);

    // Apply the default filter
    applyFilter();
    
    // After packs are loaded, fetch boxes
    await fetchBoxes();
}

function initializeBoxes(data) {
    boxes = data.map((item) => {
        const matchingPack = packs.find((pack) => pack.setNumber === parseFloat(item.setNumber));
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
            setNumber: parseFloat(item.setNumber),
            ev: ev,
            percentReturn: percentReturn,
            boxPremium: boxPremium,
        };
    });

    console.log("Boxes loaded:", boxes.length);

    // Get the most recent lastUpdated timestamp
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

    applyBoxFilter(); // Apply the default filter
}

function handleError(error) {
    console.error("Error fetching data:", error);
    const packsList = document.getElementById("packs-list");
    if (packsList) {
        packsList.innerHTML = "<li>Error loading data</li>";
    }
}

// Function to display the list of boxes
function displayPacks() {
    const ul = document.getElementById("packs-list");
    ul.innerHTML = ""; // Clear the existing list

    console.log("Displaying boxes, count:", filteredBoxes.length);

    if (filteredBoxes.length === 0) {
        ul.innerHTML = "<li>No boxes found</li>";
        return;
    }

    filteredBoxes.forEach((box) => {
        const li = document.createElement("li");
        li.className = "pack-item";
        
        // Create the box header with text and logo
        const boxHeader = document.createElement("div");
        boxHeader.className = "pack-header";
        
        // Create text content
        const textContent = document.createElement("span");
        textContent.textContent = `${box.name} - Box Price: $${box.value.toFixed(2)}, EV: $${box.ev.toFixed(2)}, Percent Return: ${box.percentReturn.toFixed(2)}%, Price Per Pack: $${box.pricePer.toFixed(2)}, Box Premium: ${box.boxPremium.toFixed(2)}%`;
        
        // Create logo image
        const logoImg = document.createElement("img");
        const setId = box.setNumber.toString().replace('.', '_');
        logoImg.src = `logos/${setId}.png`;
        logoImg.alt = `${box.name} logo`;
        logoImg.className = "pack-logo";
        
        // Fallback: hide image if logo doesn't exist
        logoImg.onerror = () => {
            logoImg.style.display = 'none';
        };
        
        // Append text and logo to header
        boxHeader.appendChild(textContent);
        boxHeader.appendChild(logoImg);
        
        li.appendChild(boxHeader);
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

// Calculate Sealed Product Value
const productValueButton = document.querySelector(".productValueButton");
if (productValueButton) {
    productValueButton.addEventListener("click", async function () {
        // Use existing packs data
        if (packs.length === 0) {
            alert("Packs data not loaded yet. Please wait and try again.");
            return;
        }

        const productPrice = parseFloat(prompt("Enter the price of the product:"));
        if (isNaN(productPrice)) {
            alert("Invalid price entered. Please enter a numeric value.");
            return;
        }

        const numberOfPacks = parseInt(prompt("Enter the number of packs in the product:"), 10);
        if (isNaN(numberOfPacks) || numberOfPacks <= 0) {
            alert("Please enter a valid number of packs!");
            return;
        }

        let packTotal = 0;
        for (let i = 0; i < numberOfPacks; i++) {
            const packName = prompt(`Enter the name of pack ${i + 1}:`);
            const pack = packs.find((p) => p.name.toLowerCase() === packName.toLowerCase());

            if (pack) {
                packTotal += parseFloat(pack.value);
                alert(`Pack '${pack.name}' with value of $${pack.value} added. Running total: $${packTotal.toFixed(2)}`);
            } else {
                alert(`Pack '${packName}' not found. Skipping.`);
            }
        }

        const totalProfit = packTotal - productPrice;
        const percentProfit = ((packTotal / productPrice) - 1) * 100;

        alert(`Total Value of packs: $${packTotal.toFixed(2)}\n` + 
              `Total Profit: $${totalProfit.toFixed(2)}\n` + 
              `Percent Profit: ${percentProfit.toFixed(2)}%`);
    });
}

// Calculate EV for a Sealed Product
const sealedProductEvButton = document.querySelector(".sealedProductEvButton");
if (sealedProductEvButton) {
    sealedProductEvButton.addEventListener("click", async function () {
        // Use existing packs data
        if (packs.length === 0) {
            alert("Packs data not loaded yet. Please wait and try again.");
            return;
        }

        const productPrice = parseFloat(prompt("Enter the price of the sealed product:"));
        if (isNaN(productPrice)) {
            alert("Invalid price entered. Please enter a numeric value.");
            return;
        }

        const numberOfPacks = parseInt(prompt("Enter the number of packs in the sealed product:"), 10);
        if (isNaN(numberOfPacks) || numberOfPacks <= 0) {
            alert("Please enter a valid number of packs!");
            return;
        }

        let packTotalEv = 0;
        for (let i = 0; i < numberOfPacks; i++) {
            const packName = prompt(`Enter the name of pack ${i + 1}:`);
            const pack = packs.find((p) => p.name.toLowerCase() === packName.toLowerCase());

            if (pack) {
                packTotalEv += parseFloat(pack.ev);
                alert(`Pack '${pack.name}' with EV of $${pack.ev} added. Running total EV: $${packTotalEv.toFixed(2)}`);
            } else {
                alert(`Pack '${packName}' not found. Skipping.`);
            }
        }

        const sealedProductEv = packTotalEv - productPrice;

        alert(`Total EV of packs: $${packTotalEv.toFixed(2)}\n` +
              `Expected Profit for the sealed product: $${sealedProductEv.toFixed(2)}`);
    });
}

// Calculate EV for Multiple Packs
const multiplePacksEvButton = document.querySelector(".multiplePacksEvButton");
if (multiplePacksEvButton) {
    multiplePacksEvButton.addEventListener("click", async function () {
        // Use existing packs data
        if (packs.length === 0) {
            alert("Packs data not loaded yet. Please wait and try again.");
            return;
        }

        let totalEv = 0;

        while (true) {
            const packName = prompt("Enter the pack name (or type 'done' to finish):").trim();
            if (packName.toLowerCase() === "done") break;

            const pack = packs.find((p) => p.name.toLowerCase() === packName.toLowerCase());

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

// Calculate EV for a Single Pack
const singlePackEvButton = document.querySelector(".singlePackEvButton");
if (singlePackEvButton) {
    singlePackEvButton.addEventListener("click", async function () {
        // Use existing packs data
        if (packs.length === 0) {
            alert("Packs data not loaded yet. Please wait and try again.");
            return;
        }

        const packName = prompt("Enter the name of the pack:").trim();
        const pack = packs.find((p) => p.name.toLowerCase() === packName.toLowerCase());

        if (pack) {
            const totalEv = parseFloat(pack.ev);
            alert(`Pack: ${pack.name}\nEV: $${totalEv.toFixed(2)}\nReturn on Investment: ${(pack.adjEv * 100).toFixed(2)}%`);
        } else {
            alert(`Pack '${packName}' not found.`);
        }
    });
}

// Fetch and initialize packs on page load (packs must load first, then boxes)
fetchPacks();

function findExactPack(packName) {
    return packs.find((pack) => pack.name.toLowerCase() === packName.toLowerCase());
}