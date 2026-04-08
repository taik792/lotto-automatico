fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    // ESTRAZIONI
    const estrDiv = document.getElementById("estrazioni");

    for (const r in data.ultime_estrazioni) {
      estrDiv.innerHTML += `
        <div class="card">
          <b>${r}</b><br>
          ${data.ultime_estrazioni[r].join(" - ")}
        </div>
      `;
    }

    // AMBI CON RUOTA
    const ambiDiv = document.getElementById("ambi");

    data.top.forEach(a => {
      ambiDiv.innerHTML += `
        <div class="card top">
          <b>${a.ruota}</b><br>
          ${a.numeri.join(" - ")}<br>
          ${a.prob}%
        </div>
      `;
    });

    // JOLLY
    const terniDiv = document.getElementById("terni");

    terniDiv.innerHTML = `
      <div class="card">
        🎯 Ruota Jolly: <b>${data.ruota_jolly}</b>
      </div>
    `;

  });