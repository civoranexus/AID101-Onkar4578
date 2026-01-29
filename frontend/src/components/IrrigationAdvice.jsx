import { useState } from "react";
import API_BASE from "../api";

function IrrigationAdvice() {
  const [soil, setSoil] = useState("");
  const [temp, setTemp] = useState("");
  const [advice, setAdvice] = useState("");

  const getAdvice = async () => {
    const res = await fetch(`${API_BASE}/irrigation-advice`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        soil_moisture: soil,
        temperature: temp
      })
    });

    const data = await res.json();
    setAdvice(data.advice);
  };

  return (
    <div>
      <h2>Irrigation Advice</h2>

      <input placeholder="Soil Moisture" onChange={(e) => setSoil(e.target.value)} />
      <input placeholder="Temperature" onChange={(e) => setTemp(e.target.value)} />

      <button onClick={getAdvice}>Get Advice</button>

      <p>{advice}</p>
    </div>
  );
}

export default IrrigationAdvice;
