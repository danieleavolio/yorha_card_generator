from consts import CHIP_PALETTE, OTHER_COLOR

def exclude_languages(
    languages: dict,
    excluded: list[str]
) -> dict:
    """Remove languages from the statistics by name (case-insensitive)."""
    names = {
        name.strip().casefold()
        for name in excluded
        if name.strip()
    }

    if not names:
        return languages

    return {
        name: size for name, size in languages.items()
        if name.casefold() not in names
    }

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
