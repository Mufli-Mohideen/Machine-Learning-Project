document
  .getElementById("predictionForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    console.log("Form Data:", data); // Check what data is being sent

    axios
      .post("/predict", data)
      .then((response) => {
        document.getElementById("result").innerText =
          "Predicted Winner: " + response.data.prediction;
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  });
