let packs = [];

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

        packs = data.map((item) => ({
            name: item.setName,
            value: item.packValue,
            ev: item.ev,
            adjEv: item.adjustedEv
        }));

        console.log("Packs loaded:", packs.length);
    } catch (error) {
        console.error("Error fetching pack data:", error);
    }
}

// Improved pack finding function with fuzzy matching
function findExactPack(packName) {
    if (!packName || !packName.trim()) {
        return null;
    }
    
    // Normalize the input
    const normalizeString = (str) => {
        return str
            .toLowerCase()
            .replace(/\s+/g, '') // Remove all spaces
            .replace(/&/g, 'and'); // Replace & with "and"
    };
    
    const normalizedInput = normalizeString(packName);
    
    // Special case mappings
    const specialCases = {
        'sunandmoon': 'SM Base Set',
        'sunmoon': 'SM Base Set',
        'sm': 'SM Base Set',
        'xy': 'XY Base Set'
    };
    
    // Check for special cases first
    if (specialCases[normalizedInput]) {
        const specialCaseName = specialCases[normalizedInput];
        const found = packs.find((pack) => 
            normalizeString(pack.name) === normalizeString(specialCaseName)
        );
        if (found) return found;
    }
    
    // First try: Exact match (after normalization)
    let found = packs.find((pack) => 
        normalizeString(pack.name) === normalizedInput
    );
    if (found) return found;
    
    // Second try: Input is contained in pack name
    const containsMatches = packs.filter((pack) => 
        normalizeString(pack.name).includes(normalizedInput)
    );
    
    // If we found matches, handle special cases
    if (containsMatches.length > 0) {
        // Special handling for "Base Set" - prioritize "Base Set" over "Base Set 2"
        if (normalizedInput === 'baseset') {
            const baseSet = containsMatches.find((pack) => 
                normalizeString(pack.name) === 'baseset' || 
                pack.name === 'Base Set'
            );
            if (baseSet) return baseSet;
        }
        
        // Return the shortest match (most specific)
        // This helps prefer "Evolving Skies" over "SWSH07: Evolving Skies"
        containsMatches.sort((a, b) => a.name.length - b.name.length);
        return containsMatches[0];
    }
    
    // Third try: Pack name contains the input
    found = packs.find((pack) => 
        normalizeString(pack.name).includes(normalizedInput)
    );
    if (found) return found;
    
    // No match found
    return null;
}

// Multiple Packs EV Calculator
let packCounter = 1;

document.getElementById('addPackBtn').addEventListener('click', function() {
    packCounter++;
    const inputsContainer = document.getElementById('multiplePacksInputs');
    const newInput = document.createElement('div');
    newInput.className = 'form-group pack-input-group';
    newInput.innerHTML = `
        <label>Pack Name:</label>
        <input type="text" class="pack-name-input" placeholder="e.g., Evolving Skies" required>
        <button type="button" class="remove-pack-btn" onclick="this.parentElement.remove()">Remove</button>
    `;
    inputsContainer.appendChild(newInput);
});

document.getElementById('multiplePacksForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const inputs = document.querySelectorAll('.pack-name-input');
    const resultDiv = document.getElementById('multiplePacksResult');
    
    let totalEv = 0;
    let totalValue = 0;
    let results = [];
    let notFound = [];
    
    inputs.forEach((input, index) => {
        const packName = input.value.trim();
        if (packName) {
            const pack = findExactPack(packName);
            if (pack) {
                totalEv += pack.ev;
                totalValue += pack.value;
                results.push(`<div class="pack-result-item">${pack.name}: EV $${pack.ev.toFixed(2)} | Value $${pack.value.toFixed(2)}</div>`);
            } else {
                notFound.push(packName);
            }
        }
    });
    
    // Calculate ROI
    const roi = totalValue > 0 ? ((totalEv / totalValue) * 100) : 0;
    
    let html = '<div class="result-success">';
    html += '<h3>Total EV Calculation</h3>';
    html += results.join('');
    html += '<div class="result-summary">';
    html += `<div class="result-row"><span class="result-label">Total Expected Value:</span><span class="result-value">$${totalEv.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Total Pack Value:</span><span class="result-value">$${totalValue.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Return on Investment:</span><span class="result-value">${roi.toFixed(2)}%</span></div>`;
    html += '</div>';
    
    if (notFound.length > 0) {
        html += `<div class="result-warning">Not found: ${notFound.join(', ')}</div>`;
    }
    html += '</div>';
    
    resultDiv.innerHTML = html;
});

// Combined Sealed Product Calculator (Market Value + EV)
document.getElementById('numPacksValue').addEventListener('change', function() {
    const numPacks = parseInt(this.value);
    const container = document.getElementById('productValuePackInputs');
    container.innerHTML = '';
    
    if (numPacks > 0) {
        for (let i = 0; i < numPacks; i++) {
            const input = document.createElement('div');
            input.className = 'form-group';
            input.innerHTML = `
                <label>Pack ${i + 1} Name:</label>
                <input type="text" class="product-pack-input" placeholder="e.g., Evolving Skies" required>
            `;
            container.appendChild(input);
        }
    }
});

document.getElementById('productValueForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const productPrice = parseFloat(document.getElementById('productPrice').value);
    const inputs = document.querySelectorAll('.product-pack-input');
    const resultDiv = document.getElementById('productValueResult');
    
    let packTotal = 0;
    let packTotalEv = 0;
    let results = [];
    let notFound = [];
    
    inputs.forEach((input, index) => {
        const packName = input.value.trim();
        if (packName) {
            const pack = findExactPack(packName);
            if (pack) {
                packTotal += pack.value;
                packTotalEv += pack.ev;
                results.push(`<div class="pack-result-item">${pack.name}: Value $${pack.value.toFixed(2)} | EV $${pack.ev.toFixed(2)}</div>`);
            } else {
                notFound.push(packName);
            }
        }
    });
    
    const totalProfit = packTotal - productPrice;
    const percentProfit = ((packTotal / productPrice) - 1) * 100;
    const expectedProfit = packTotalEv - productPrice;
    const percentReturnEv = ((packTotalEv / productPrice) - 1) * 100;
    
    let html = '<div class="result-success">';
    html += '<h3>Sealed Product Analysis</h3>';
    
    // Pack details
    html += '<div class="pack-details-section">';
    html += '<h4>Pack Breakdown:</h4>';
    html += results.join('');
    html += '</div>';
    
    // Market Value Section
    html += '<div class="value-section">';
    html += '<h4>Market Value Analysis:</h4>';
    html += `<div class="result-row"><span class="result-label">Total Pack Market Value:</span><span class="result-value">$${packTotal.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Product Price:</span><span class="result-value">$${productPrice.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Market Value Profit/Loss:</span><span class="result-value ${totalProfit >= 0 ? 'positive' : 'negative'}">$${totalProfit.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Market Value Return:</span><span class="result-value ${percentProfit >= 0 ? 'positive' : 'negative'}">${percentProfit.toFixed(2)}%</span></div>`;
    html += '</div>';
    
    // EV Section
    html += '<div class="ev-section">';
    html += '<h4>Expected Value Analysis:</h4>';
    html += `<div class="result-row"><span class="result-label">Total Pack EV:</span><span class="result-value">$${packTotalEv.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Product Price:</span><span class="result-value">$${productPrice.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Expected Profit/Loss:</span><span class="result-value ${expectedProfit >= 0 ? 'positive' : 'negative'}">$${expectedProfit.toFixed(2)}</span></div>`;
    html += `<div class="result-row"><span class="result-label">Expected Value Return:</span><span class="result-value ${percentReturnEv >= 0 ? 'positive' : 'negative'}">${percentReturnEv.toFixed(2)}%</span></div>`;
    html += '</div>';
    
    if (notFound.length > 0) {
        html += `<div class="result-warning">Not found: ${notFound.join(', ')}</div>`;
    }
    html += '</div>';
    
    resultDiv.innerHTML = html;
});


// Fetch packs on page load
fetchPacks();