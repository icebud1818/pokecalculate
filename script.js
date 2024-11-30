let packs = [];
let filteredPacks = []; // To hold the currently filtered packs
let activeFilter = "all"; // To track the active filter
let lastSortCriteria = "nameAsc"; // To track the last sorting criteria
const packsDataUrl = "full_output_with_all_columns.json";


// Fetch packs data and populate the initial list
function fetchPacks() {
    if (window.fetch) {
        fetch(packsDataUrl)
            .then((response) => response.json())
            .then((data) => initializePacks(data))
            .catch(handleError);
    } else {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", packsDataUrl, true);
        xhr.onload = function () {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                initializePacks(data);
            } else {
                handleError(xhr.statusText);
            }
        };
        xhr.onerror = () => handleError("Network Error");
        xhr.send();
    }
}

function initializePacks(data) {
    packs = data.map((item) => ({
        name: item["Set Name"],
        value: item["Pack Value"],
        ev: item["EV"],
        adjEv: item["Adj. EV"],
        setNumber: parseInt(item["SetNumber"], 10),
    }));

    const lastUpdated = data[0]["Last Updated"];
    document.getElementById("lastUpdated").textContent = `Last Updated: ${lastUpdated}`;

    applyFilter(); // Apply the default filter (all packs)
}

function handleError(error) {
    console.error("Error fetching pack data:", error);
    document.getElementById("packs-list").innerHTML = "<li>Error loading packs</li>";
}

// Function to display the list of packs
function displayPacks() {
    const ul = document.getElementById("packs-list");
    ul.innerHTML = ""; // Clear the existing list

    filteredPacks.forEach((pack) => {
        const li = document.createElement("li");
        li.textContent = `${pack.name} - Value: $${pack.value.toFixed(2)} - EV: $${pack.ev.toFixed(
            2
        )} - Percent Return: ${(pack.adjEv * 100).toFixed(2)}%`;
        ul.appendChild(li);
    });
}

// Function to handle sorting based on selected criteria
function sortPacks(criteria) {
    const sorters = {
        nameAsc: (a, b) => a.name.localeCompare(b.name),
        nameDesc: (a, b) => b.name.localeCompare(a.name),
        valueAsc: (a, b) => a.value - b.value,
        valueDesc: (a, b) => b.value - a.value,
        evAsc: (a, b) => a.ev - b.ev,
        evDesc: (a, b) => b.ev - a.ev,
        adjEvAsc: (a, b) => a.adjEv - b.adjEv,
        adjEvDesc: (a, b) => b.adjEv - a.adjEv,
        setNumberAsc: (a, b) => a.setNumber - b.setNumber,
        setNumberDesc: (a, b) => b.setNumber - a.setNumber,
    };

    if (sorters[criteria]) {
        lastSortCriteria = criteria; // Update the sorting criteria
        filteredPacks.sort(sorters[criteria]); // Sort the currently filtered packs
        displayPacks(); // Refresh the list
    } else {
        console.error("Invalid sort criteria:", criteria);
    }
}

// Function to filter packs based on the selected criteria
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
    };

    if (filterers[activeFilter]) {
        filteredPacks = filterers[activeFilter](); // Apply the selected filter
        sortPacks(lastSortCriteria); // Reapply the last sorting
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
    applyFilter(); // Apply the new filter
});

// Fetch and initialize packs on page load
fetchPacks();



// Add your calculation buttons here (kept unchanged)

// Sealed Product Value Calculation
document.getElementById("productValueButton").addEventListener("click", function () {
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
        const pack = findExactPack(packName);

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
document.getElementById("sealedProductEvButton").addEventListener("click", function () {
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
        const pack = findExactPack(packName);

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
document.getElementById("multiplePacksEvButton").addEventListener("click", function () {
    let totalEv = 0;

    while (true) {
        const packName = prompt("Enter the pack name (or type 'done' to finish):").trim();
        if (packName.toLowerCase() === "done") break;

        const pack = findExactPack(packName);

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
document.getElementById("singlePackEvButton").addEventListener("click", function () {
    const packName = prompt("Enter the name of the pack:").trim();
    const pack = findExactPack(packName);

    if (pack) {
        const totalEv = parseFloat(pack.ev); // EV for a single pack
        alert(`Pack: ${pack.name}\nEV: $${totalEv.toFixed(2)}\nReturn on Investment: ${(pack.adjEv * 100).toFixed(2)}%`);
    } else {
        alert(`Pack '${packName}' not found.`);
    }
});

function findExactPack(packName) {
    return packs.find((pack) => pack.name.toLowerCase() === packName.toLowerCase());
}
