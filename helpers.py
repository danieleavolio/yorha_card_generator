from consts import CHIP_PALETTE, OTHER_COLOR

def calculate_language_percentages(
    languages: dict,
    limit: int = 5
) -> list:
    total = sum(languages.values())

    if total <= 0:
        return []

    ordered = sorted(
        languages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_languages = ordered[:limit]

    result = []

    for index, (name, size) in enumerate(top_languages):
        result.append({
            "name": name,
            "bytes": size,
            "percentage": (size / total) * 100,
            "color": CHIP_PALETTE[
                index % len(CHIP_PALETTE)
            ]
        })

    # Aggregate all remaining languages.
    remaining = sum(
        size for _, size in ordered[limit:]
    )

    if remaining > 0:
        result.append({
            "name": "Other",
            "bytes": remaining,
            "percentage": (remaining / total) * 100,
            "color": OTHER_COLOR
        })

    return result
