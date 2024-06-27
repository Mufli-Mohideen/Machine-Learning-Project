document
  .getElementById("predictionForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
      team1: document.getElementById("team1").value,
      team2: document.getElementById("team2").value,
      venue: document.getElementById("venue").value,
      total_runs: document.getElementById("total_runs").value,
      balls_faced: document.getElementById("balls_faced").value,
    };

    fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById(
          "result"
        ).innerText = `Prediction: ${data.prediction}`;
      })
      .catch((error) => console.error("Error:", error));
  });
