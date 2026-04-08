fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // 🔥 ULTIMA ESTRAZIONE
    const estrDiv = document.getElementById("estrazione");

    estrDiv.innerHTML = `
      <div class="estrazione">
        <h3>🧾 Ultima Estrazione</h3>
        <p>${data.ultima_estrazione.join(" - ")}</p>
      </div>
    `;

    // ⭐ TOP
    const topDiv = document.getElementById("top");

    data.top.forEach(item => {
      const div = document.createElement("div");
      div.className = "card top";

      div.innerHTML = `
        <h2>🔥 ${item.ambo[0]} - ${item.ambo[1]}</h2>
        <p>Score: ${item.score}</p>
      `;

      topDiv.appendChild(div);
    });

    // 🎯 AMBI
    const container = document.getElementById("giocate");

    data.ambi.forEach(item => {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <h3>${item.ambo[0]} - ${item.ambo[1]}</h3>
        <p>Score: ${item.score}</p>
      `;

      container.appendChild(div);
    });

  });