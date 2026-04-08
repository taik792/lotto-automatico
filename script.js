fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // ESTRAZIONI (CARD)
    const estrDiv = document.getElementById("estrazioni");

    for (const r in data.ultime_estrazioni) {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <div class="small">${r}</div>
        <div>${data.ultime_estrazioni[r].join(" - ")}</div>
      `;

      estrDiv.appendChild(div);
    }

    // GEMELLE (COMPATTE)
    const gemDiv = document.getElementById("gemelle");

    let txt = "";
    for (const r in data.ruote_gemelle) {
      txt += `${r} → ${data.ruote_gemelle[r]}<br>`;
    }
    gemDiv.innerHTML = txt;

    // AMBI
    const ambiDiv = document.getElementById("ambi");

    data.top_ambi.forEach(a => {
      const div = document.createElement("div");
      div.className = "card top";

      div.innerHTML = `
        <div class="highlight">${a.numeri.join(" - ")}</div>
        <div class="small">${a.prob}%</div>
      `;

      ambiDiv.appendChild(div);
    });

    // TERNI
    const terniDiv = document.getElementById("terni");

    data.top_terni.forEach(t => {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <div class="highlight">${t.numeri.join(" - ")}</div>
        <div class="small">${t.prob}%</div>
      `;

      terniDiv.appendChild(div);
    });

  });