fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // ESTRAZIONI
    const estrDiv = document.getElementById("estrazioni");
    estrDiv.innerHTML = "<h3>Ultime Estrazioni</h3>";

    for (const r in data.ultime_estrazioni) {
      estrDiv.innerHTML += `<p>${r}: ${data.ultime_estrazioni[r].join(" - ")}</p>`;
    }

    // GEMELLE
    const gemDiv = document.getElementById("gemelle");
    gemDiv.innerHTML = "<h3>Ruote Gemelle</h3>";

    for (const r in data.ruote_gemelle) {
      gemDiv.innerHTML += `<p>${r} → ${data.ruote_gemelle[r]}</p>`;
    }

    // AMBI
    const ambiDiv = document.getElementById("ambi");

    data.top_ambi.forEach(a => {
      ambiDiv.innerHTML += `
        <div class="card top">
          ${a.numeri.join(" - ")}<br>
          ${a.prob}%
        </div>
      `;
    });

    // TERNI
    const terniDiv = document.getElementById("terni");

    data.top_terni.forEach(t => {
      terniDiv.innerHTML += `
        <div class="card">
          ${t.numeri.join(" - ")}<br>
          ${t.prob}%
        </div>
      `;
    });

  });