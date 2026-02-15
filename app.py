<script>
async function caricaDati() {
    try {
        const response = await fetch("https://lotto-statistiche.onrender.com/api");
        
        if (!response.ok) {
            throw new Error("Errore risposta server");
        }

        const dati = await response.json();
        console.log(dati);

        const container = document.getElementById("contenuto");
        container.innerHTML = "";

        for (let ruota in dati) {
            const div = document.createElement("div");
            div.innerHTML = `
                <h2>${ruota}</h2>
                <p>Ultima estrazione: ${dati[ruota].ultima_estrazione.join(", ")}</p>
                <p>Previsione: ${dati[ruota].previsione.join(", ")}</p>
                <hr>
            `;
            container.appendChild(div);
        }

    } catch (error) {
        console.error(error);
        document.getElementById("contenuto").innerHTML = "Errore caricamento dati";
    }
}

caricaDati();
</script>








