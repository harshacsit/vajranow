def get_alert_level(
    thunderstorm_probability,
    lightning_probability
):
    combined_risk = (
        thunderstorm_probability * 0.7
        + lightning_probability * 0.3
    )

    if combined_risk >= 75:

        return {
            "level": "SEVERE",
            "icon": "🔴",
            "action": "Immediate preparedness recommended"
        }

    elif combined_risk >= 50:

        return {
            "level": "WARNING",
            "icon": "🟠",
            "action": "Prepare for possible severe weather"
        }

    elif combined_risk >= 30:

        return {
            "level": "WATCH",
            "icon": "🟡",
            "action": "Monitor developing conditions"
        }

    else:

        return {
            "level": "LOW",
            "icon": "🟢",
            "action": "No significant risk detected"
        }
        