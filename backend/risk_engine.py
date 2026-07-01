def clamp(value, low=0, high=100):
    return max(low, min(high, float(value)))


def risk_level(score):
    score = float(score)

    if score >= 70:
        return "High"

    if score >= 40:
        return "Medium"

    return "Low"


def flood_score(t1=0, t3=0, t7=0, live_precipitation=0):
    score = (
        float(t1) * 0.50
        + float(t3) * 0.30
        + float(t7) * 0.20
        + float(live_precipitation) * 3
    )

    return clamp(score)


def drought_score(t7=0, temperature=30):
    score = 100 - float(t7) * 8 + max(0, float(temperature) - 35) * 8
    return clamp(score)


def flood_advisory(score):
    level = risk_level(score)

    if level == "High":
        return "High flood risk. Monitor low-lying regions and issue early warnings."

    if level == "Medium":
        return "Moderate flood risk. Continue rainfall monitoring in vulnerable areas."

    return "Low flood risk. No immediate flood alert."


def drought_advisory(score):
    level = risk_level(score)

    if level == "High":
        return "High drought stress. Recommend irrigation support and crop monitoring."

    if level == "Medium":
        return "Moderate drought risk. Monitor rainfall deficit and water stress."

    return "Low drought risk. Conditions appear stable."