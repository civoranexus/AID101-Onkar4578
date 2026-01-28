def recommend_fertilizer(soil_type, crop_stage, nitrogen, phosphorus, potassium):
    recommendation = []
    explanation = []

    if nitrogen < 50:
        recommendation.append("Urea")
        explanation.append("Low nitrogen detected")

    if phosphorus < 40:
        recommendation.append("DAP")
        explanation.append("Low phosphorus detected")

    if potassium < 45:
        recommendation.append("MOP")
        explanation.append("Low potassium detected")

    if crop_stage.lower() in ["flowering", "fruiting"]:
        explanation.append("Critical growth stage requires balanced nutrients")

    if not recommendation:
        return {
            "fertilizer_required": False,
            "message": "Soil nutrients are sufficient",
            "explanation": "No fertilizer application needed at this stage"
        }

    return {
        "fertilizer_required": True,
        "recommended_fertilizers": recommendation,
        "explanation": ", ".join(explanation)
    }
