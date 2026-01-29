import { useState } from "react";
import API_BASE from "../api";

function FarmerForm() {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [soilType, setSoilType] = useState("");

  const submitFarmer = async () => {
    await fetch(`${API_BASE}/add-farmer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name,
        location: location,
        soil_type: soilType
      })
    });

    alert("Farmer Added");
  };

  return (
    <div>
      <h2>Add Farmer</h2>
      <input placeholder="Name" onChange={(e) => setName(e.target.value)} />
      <input placeholder="Location" onChange={(e) => setLocation(e.target.value)} />
      <input placeholder="Soil Type" onChange={(e) => setSoilType(e.target.value)} />
      <button onClick={submitFarmer}>Add</button>
    </div>
  );
}

export default FarmerForm;
