from alert_engine import get_alert_level


tests = [
    (20, 10),
    (45, 35),
    (65, 60),
    (90, 85)
]


print()
print("===================================")
print(" VajraNow Alert Engine")
print("===================================")


for thunderstorm, lightning in tests:

    result = get_alert_level(
        thunderstorm,
        lightning
    )

    print()
    print(
        f"Thunderstorm Risk : {thunderstorm}%"
    )

    print(
        f"Lightning Risk    : {lightning}%"
    )

    print(
        f"Alert             : "
        f"{result['icon']} {result['level']}"
    )

    print(
        f"Action            : "
        f"{result['action']}"
    )


print()
print("===================================")