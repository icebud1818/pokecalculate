let packs = [];
let filteredPacks = []; // To hold the currently filtered packs
let activeFilter = "all"; // To track the active filter
let lastSortCriteria = "nameAsc"; // To track the last sorting criteria
const packsDataUrl = "boxData.json";


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
        value: item["Box Price"],
        pricePer: item["Price Per"],
        setNumber: parseInt(item["Set Number"], 10),
    }));

    const lastUpdated = data[0]["Last Updated"];
    document.getElementById("lastUpdated").textContent = `Last Updated: ${lastUpdated} UTC`;

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
        li.textContent = `${pack.name} - Box Price: $${pack.value.toFixed(2)} - Price Per Pack: $${pack.pricePer.toFixed(
            2
        )} - Box Premium: %`;
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
        evAsc: (a, b) => a.pricePer - b.pricePer,
        evDesc: (a, b) => b.pricePer - a.pricePer,
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
        gen6: () => packs.filter((pack) => pack.setNumber >= 0 && pack.setNumber <= 12),
        gen7: () => packs.filter((pack) => pack.setNumber >= 13 && pack.setNumber <= 24),
        gen8: () => packs.filter((pack) => pack.setNumber >= 25 && pack.setNumber <= 36),
        gen9: () => packs.filter((pack) => pack.setNumber >= 37 && pack.setNumber <= 44)
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

function findExactPack(packName) {
    return packs.find((pack) => pack.name.toLowerCase() === packName.toLowerCase());
}
