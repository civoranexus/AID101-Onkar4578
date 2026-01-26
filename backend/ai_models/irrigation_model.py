def recommend_irrigation(rainfall, temperature, soil_moisture, crop_stage):
   

    water_needed = 0
    explanation = []

    if rainfall < 500:
        water_needed += 30
        explanation.append("Low rainfall detected")

    if temperature > 30:
        water_needed += 20
        explanation.append("High temperature increases evaporation")

    if soil_moisture < 40:
        water_needed += 25
        explanation.append("Low soil moisture level")

    if crop_stage.lower() in ["flowering", "fruiting"]:
        water_needed += 15
        explanation.append("Critical crop growth stage")

    if water_needed == 0:
        return {
            "irrigation_required": False,
            "water_liters_per_acre": 0,
            "message": "No irrigation required today"
        }

    return {
        "irrigation_required": True,
        "water_liters_per_acre": water_needed,
        "message": ", ".join(explanation)
    }
