fetch("risultati.json")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("giocate");

    container.innerHTML = "";

    data.forEach(item => {

      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <h3>🎯 ${item.ambo[0]} - ${item.ambo[1]}</h3>
        <p>Score: ${item.score}</p>
      `;

      container.appendChild(div);
    });

  })
  .catch(err => console.error(err));