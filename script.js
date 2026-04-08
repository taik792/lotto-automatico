fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // 🧾 ESTRAZIONI
    const estrDiv = document.getElementById("estrazioni");

    for (const r in data.ultime_estrazioni) {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <div class="title-small">${r}</div>
        <div class="numbers">${data.ultime_estrazioni[r].join(" - ")}</div>
      `;

      estrDiv.appendChild(div);
    }

    // 🔗 GEMELLE
    const gemDiv = document.getElementById("gemelle");

    for (const r in data.ruote_gemelle) {
      const div = document.createElement("div");
      div.innerHTML = `${r} → ${data.ruote_gemelle[r]}`;
      gemDiv.appendChild(div);
    }

    // ⭐ AMBI
    const ambiDiv = document.getElementById("ambi");

    data.top_ambi.forEach(a => {
      const div = document.createElement("div");
      div.className = "card top";

      div.innerHTML = `
        <div class="numbers">${a.numeri.join(" - ")}</div>
        <div class="percent">${a.prob}%</div>
      `;

      ambiDiv.appendChild(div);
    });

    // 🔥 TERNI
    const terniDiv = document.getElementById("terni");

    data.top_terni.forEach(t => {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <div class="numbers">${t.numeri.join(" - ")}</div>
        <div class="percent">${t.prob}%</div>
      `;

      terniDiv.appendChild(div);
    });

  });