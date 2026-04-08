fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    const estrDiv = document.getElementById("estrazioni");
    const ambiDiv = document.getElementById("ambi");
    const terniDiv = document.getElementById("terni");

    estrDiv.innerHTML = "";
    ambiDiv.innerHTML = "";
    terniDiv.innerHTML = "";

    // ESTRAZIONI
    for (const r in data.ultime_estrazioni) {
      estrDiv.innerHTML += `
        <div class="card">
          <b>${r}</b><br>
          ${data.ultime_estrazioni[r].join(" - ")}
        </div>
      `;
    }

    // AMBI
    data.top_ambi.forEach(a => {
      ambiDiv.innerHTML += `
        <div class="card top">
          <b>${a.ruota}</b><br>
          ${a.numeri.join(" - ")}<br>
          ${a.prob}%
        </div>
      `;
    });

    // JOLLY
    terniDiv.innerHTML = `
      <div class="card">
        🎯 RUOTA JOLLY<br>
        <b>${data.ruota_jolly}</b>
      </div>
    `;
  });