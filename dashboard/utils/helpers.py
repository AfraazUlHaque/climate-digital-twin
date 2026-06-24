def get_risk_level(temp):

    if temp >= 6:
        return "Extreme"
    elif temp >= 4:
        return "High"
    elif temp >= 2:
        return "Moderate"

    return "Low"