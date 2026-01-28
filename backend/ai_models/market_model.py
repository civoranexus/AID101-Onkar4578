def market_advisory(current_price, avg_price, demand_index):
    """
    Simple explainable logic for market decision
    demand_index: 1 (low) to 10 (high)
    """

    if current_price > avg_price and demand_index >= 7:
        return {
            "advice": "SELL",
            "reason": "High demand and favorable market price"
        }

    if current_price < avg_price and demand_index <= 4:
        return {
            "advice": "HOLD",
            "reason": "Low demand and unfavorable price"
        }

    return {
        "advice": "WAIT",
        "reason": "Market conditions are moderate"
    }
