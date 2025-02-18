async function fetchComputers() {
    const computerList = document.getElementById("computer-list");
    const errorMessage = document.getElementById("error-message");
    errorMessage.innerText = "";
    computerList.innerHTML = "<li>📡 Chargement...</li>";

    try {
        const response = await fetch("http://127.0.0.1:5000/computers");
        const data = await response.json();
        console.log(data);

        if (data.error) {
            throw new Error(data.error);
        }

        if (data.computers && Array.isArray(data.computers)) {
            computerList.innerHTML = "";
            data.computers.forEach(computer => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<button onclick="viewLogs('${computer}')">${computer}</button>`;
                computerList.appendChild(listItem);
            });
        } else {
            throw new Error("La réponse de l'API ne contient pas un tableau valide d'ordinateurs.");
        }
    } catch (error) {
        errorMessage.innerText = error.message;
        computerList.innerHTML = "<li style='color: red;'>Erreur lors du chargement des ordinateurs</li>";
    }
}

function viewLogs(computerId) {
    window.location.href = `logs.html?computer=${computerId}`;
}

window.onload = fetchComputers;
