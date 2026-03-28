// FORM SUBMIT
const form = document.getElementById("predictForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const radius = document.getElementById("radius").value;
    const mass = document.getElementById("mass").value;
    const temperature = document.getElementById("temperature").value;
    const distance = document.getElementById("distance").value;

    const helpBox = document.getElementById("helpBox");
    const resultBox = document.getElementById("result");

    // VALIDATION
    if (!radius || !mass || !temperature || !distance) {
        helpBox.innerText = "⚠️ Please fill all fields!";
        helpBox.className = "alert alert-danger mt-3";
        return;
    }

    // LOADING MESSAGE
    helpBox.innerText = "⏳ Processing your data...";
    helpBox.className = "alert alert-warning mt-3";

    try {
        // CALL BACKEND API
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                radius,
                mass,
                temperature,
                distance
            })
        });

        const data = await response.json();

        // SHOW RESULT
        resultBox.innerText = "🌍 Result: " + data.prediction;

        helpBox.innerText = "✅ Prediction complete!";
        helpBox.className = "alert alert-success mt-3";

    } catch (error) {
        helpBox.innerText = "❌ Error connecting to server!";
        helpBox.className = "alert alert-danger mt-3";
    }
});


// DOWNLOAD FUNCTION
function downloadResult() {
    const resultText = document.getElementById("result").innerText;

    if (!resultText) {
        alert("No result to download!");
        return;
    }

    const blob = new Blob([resultText], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "ExoHabitAI_Result.txt";
    link.click();
}


// AI HELP BOX CLICK
const aiBox = document.getElementById("aiBox");

aiBox.addEventListener("click", () => {
    alert("👋 Enter planetary data like:\n\nRadius: 1.0\nMass: 1.0\nTemperature: 288\nDistance: 1 AU");
}); 
