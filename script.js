fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // 🔥 ESTRAZIONI PER RUOTA
    const estrDiv = document.getElementById("estrazione");
    estrDiv.innerHTML = "<h3>🧾 Ultime Estrazioni</h3>";

    for (const ruota in data.ultime_estrazioni) {

      const numeri = data.ultime_estrazioni[ruota];

      const div = document.createElement("div");
      div.className = "estrazione";

      div.innerHTML = `
        <strong>${ruota}</strong><br>
        ${numeri.join(" - ")}
      `;

      estrDiv.appendChild(div);
    }

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