let packs = [];
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
        setNumber: parseFloat(item.setNumber),
        top5Cards: item.top5Cards || []
    }));

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

    applyFilter();
}

function handleError(error) {
    console.error("Error fetching pack data:", error);
    document.getElementById("packs-list").innerHTML = "<li>Error loading packs</li>";
}

function displayPacks() {
    const ul = document.getElementById("packs-list");
    ul.innerHTML = "";
    
    console.log("Displaying packs, count:", filteredPacks.length);

    filteredPacks.forEach((pack, packIndex) => {
        const li = document.createElement("li");
        li.className = "pack-item";
        
        // Create main pack info (clickable)
        const packHeader = document.createElement("div");
        packHeader.className = "pack-header";
        packHeader.setAttribute("data-pack-index", packIndex);
        packHeader.textContent = `${pack.name} - Value: $${pack.value.toFixed(2)} - EV: $${pack.ev.toFixed(2)} - Percent Return: ${(pack.adjEv * 100).toFixed(2)}%`;
        
        // Create expandable details section
        const detailsSection = document.createElement("div");
        detailsSection.className = "pack-details";
        detailsSection.setAttribute("data-pack-index", packIndex);
        detailsSection.style.display = "none";
        
        // Buy indicator
        const percentReturn = pack.adjEv * 100;
        let buyIndicator = "";
        let buyClass = "";
        
        if (percentReturn >= 80) {
            buyIndicator = "Strong Buy";
            buyClass = "strong-buy";
        } else if (percentReturn >= 60) {
            buyIndicator = "Moderate Buy";
            buyClass = "moderate-buy";
        } else if (percentReturn >= 40) {
            buyIndicator = "OK Buy";
            buyClass = "ok-buy";
        } else if (percentReturn >= 20) {
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
        
        // Top 5 cards
        if (pack.top5Cards && pack.top5Cards.length > 0) {
            const top5Title = document.createElement("h4");
            top5Title.textContent = "Top 5 Most Expensive Cards:";
            top5Title.style.marginTop = "15px";
            top5Title.style.marginBottom = "10px";
            detailsSection.appendChild(top5Title);
            
            const cardsList = document.createElement("ul");
            cardsList.className = "top5-cards-list";
            
            pack.top5Cards.forEach((card, index) => {
                const cardItem = document.createElement("li");
                cardItem.textContent = `${card.name} - #${card.number} - $${card.price.toFixed(2)}`;
                cardsList.appendChild(cardItem);
            });
            
            detailsSection.appendChild(cardsList);
        }
        
        // Close button
        const closeButton = document.createElement("button");
        closeButton.textContent = "Close";
        closeButton.className = "close-details-btn";
        closeButton.setAttribute("data-pack-index", packIndex);
        closeButton.type = "button";
        
        detailsSection.appendChild(closeButton);
        
        li.appendChild(packHeader);
        li.appendChild(detailsSection);
        ul.appendChild(li);
    });
    
    // Use event delegation - attach click handlers to the parent ul
    // This is more reliable across all browsers
    ul.addEventListener("click", handlePackListClick);
    
    console.log("Finished displaying packs");
}

// Event delegation handler for Safari compatibility
function handlePackListClick(event) {
    const target = event.target;
    
    // Handle pack header clicks
    if (target.classList.contains("pack-header")) {
        const packIndex = parseInt(target.getAttribute("data-pack-index"));
        const detailsSection = target.nextElementSibling;
        
        console.log("Pack header clicked:", filteredPacks[packIndex].name);
        
        const isExpanded = detailsSection.style.display === "block";
        detailsSection.style.display = isExpanded ? "none" : "block";
        target.classList.toggle("expanded", !isExpanded);
    }
    
    // Handle close button clicks
    if (target.classList.contains("close-details-btn")) {
        event.stopPropagation();
        const packIndex = parseInt(target.getAttribute("data-pack-index"));
        const detailsSection = target.parentElement;
        const packHeader = detailsSection.previousElementSibling;
        
        console.log("Close button clicked");
        
        detailsSection.style.display = "none";
        packHeader.classList.remove("expanded");
    }
}

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
        lastSortCriteria = criteria;
        filteredPacks.sort(sorters[criteria]);
        
        // Remove old event listener before re-rendering
        const ul = document.getElementById("packs-list");
        ul.removeEventListener("click", handlePackListClick);
        
        displayPacks();
    } else {
        console.error("Invalid sort criteria:", criteria);
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
        gen8: () => packs.filter((pack) => pack.setNumber >= 1000 && pack.setNumber <= 1104),
        gen9: () => packs.filter((pack) => pack.setNumber >= 1200 && pack.setNumber <= 1215),
        special: () => packs.filter((pack) => pack.setNumber % 1 !== 0)
    };

    if (filterers[activeFilter]) {
        filteredPacks = filterers[activeFilter]();
        sortPacks(lastSortCriteria);
    } else {
        console.error("Invalid filter criteria:", activeFilter);
    }
}

function findExactPack(packName) {
    return packs.find((pack) => pack.name.toLowerCase() === packName.toLowerCase());
}

document.getElementById("sortDropdown").addEventListener("change", (event) => {
    const sortCriteria = event.target.value;
    sortPacks(sortCriteria);
});

document.getElementById("filterDropdown").addEventListener("change", (event) => {
    activeFilter = event.target.value;
    applyFilter();
});

// Sealed Product Value Calculation
document.querySelector(".productValueButton").addEventListener("click", function () {
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
document.querySelector(".sealedProductEvButton").addEventListener("click", function () {
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
document.querySelector(".multiplePacksEvButton").addEventListener("click", function () {
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
document.querySelector(".singlePackEvButton").addEventListener("click", function () {
    const packName = prompt("Enter the name of the pack:").trim();
    const pack = findExactPack(packName);

    if (pack) {
        const totalEv = parseFloat(pack.ev);
        alert(`Pack: ${pack.name}\nEV: $${totalEv.toFixed(2)}\nReturn on Investment: ${(pack.adjEv * 100).toFixed(2)}%`);
    } else {
        alert(`Pack '${packName}' not found.`);
    }
});

// Fetch and initialize packs on page load
fetchPacks();