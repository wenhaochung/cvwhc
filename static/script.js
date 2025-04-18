document.getElementById("predictButton").addEventListener("click", function() {
    const inputData = {
        category_anomaly: parseInt(document.getElementById("category_anomaly").value),
        maker: document.getElementById("Maker").value,
        model: document.getElementById("Model").value,
        seatCount: parseInt(document.getElementById("Seat_num").value),
        doorCount: parseInt(document.getElementById("Door_num").value),
        repairCost: parseFloat(document.getElementById("repair_cost").value),
        repairHours: parseFloat(document.getElementById("repair_hours").value),
        repairComplexity: parseInt(document.getElementById("repair_complexity").value),
    };
    fetch('https://cvwhc.fly.dev/predict', {  // Updated to Fly.io URL
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(inputData)
    })
    .then(response =>{ 
        if(!response.ok) {
            return response.text().then(text => { throw new Error(text) })
           }
          else {
           return response.json();
          }
    })
    .then(data => {
        document.getElementById("result").innerText = `Prediction Result: ${data.prediction} (Probability: ${(data.probability * 100).toFixed(1)}%)`;
    })
    .catch(error => {
        try {
            const errorObj = JSON.parse(error.message);
            document.getElementById("error").innerText = errorObj.error;
        } catch (e) {
            document.getElementById("error").innerText = error.message;
        }
    });
});