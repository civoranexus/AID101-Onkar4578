import { useEffect, useState } from "react";
import API_BASE from "../api";

function FarmerList() {
  const [farmers, setFarmers] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/farmers`)
      .then(res => res.json())
      .then(data => setFarmers(data));
  }, []);

  return (
    <div>
      <h2>Farmers List</h2>
      <ul>
        {farmers.map(f => (
          <li key={f.id}>
            {f.name} - {f.location} - {f.soil_type}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FarmerList;
