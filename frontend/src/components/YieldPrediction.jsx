import { useState } from "react";
import API_BASE from "../api";

function YieldPrediction() {
  const [rainfall, setRainfall] = useState("");
  const [temperature, setTemperature] = useState("");
  const [soilQuality, setSoilQuality] = useState("");
  const [result, setResult] = useState("");

  const predict = async () => {
    const res = await fetch(`${API_BASE}/predict-yield`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rainfall,
        temperature,
        soil_quality: soilQuality
      })
    });

    const data = await res.json();
    setResult(data.predicted_yield_kg_per_acre);
  };

  return (
    <div>
      <h2>Yield Prediction</h2>

      <input placeholder="Rainfall" onChange={(e) => setRainfall(e.target.value)} />
      <input placeholder="Temperature" onChange={(e) => setTemperature(e.target.value)} />
      <input placeholder="Soil Quality" onChange={(e) => setSoilQuality(e.target.value)} />

      <button onClick={predict}>Predict</button>

      <p>Predicted Yield: {result}</p>
    </div>
  );
}

export default YieldPrediction;
