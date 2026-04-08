fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    console.log("DEBUG:", data); // 👈 utile se qualcosa va male

    // 🔥 ULTIMA ESTRAZIONE
    const estrDiv = document.getElementById("estrazione");

    if (data.ultima_estrazione) {
      estrDiv.innerHTML = `
        <div class="estrazione">
          <h3>🧾 Ultima Estrazione</h3>
          <p>${data.ultima_estrazione.join(" - ")}</p>
        </div>
      `;
    }

    // ⭐ TOP
    const topDiv = document.getElementById("top");
    topDiv.innerHTML = "";

    if (data.top && data.top.length > 0) {
      data.top.forEach(item => {
        const div = document.createElement("div");
        div.className = "card top";

        div.innerHTML = `
          <h2>🔥 ${item.ambo[0]} - ${item.ambo[1]}</h2>
          <p>Score: ${item.score}</p>
        `;

        topDiv.appendChild(div);
      });
    }

    // 🎯 AMBI
    const container = document.getElementById("giocate");
    container.innerHTML = "";

    if (data.ambi && data.ambi.length > 0) {
      data.ambi.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
          <h3>${item.ambo[0]} - ${item.ambo[1]}</h3>
          <p>Score: ${item.score}</p>
        `;

        container.appendChild(div);
      });
    }

  })
  .catch(err => console.error("Errore:", err));