import argparse
import os
from urllib.error import HTTPError, URLError
from api import get_languages
from helpers import (
    calculate_language_percentages,
    exclude_languages
)
from renderer import render_languages_card
from consts import THEMES

def parse_args():
    parser = argparse.ArgumentParser(
        description="YoRHa Card Generator"
    )

    parser.add_argument('--username',required=True)
    parser.add_argument(
        '--exclude-languages',
        default=os.getenv('EXCLUDED_LANGUAGES', ''),
        help='Comma-separated language names to ignore '
             '(e.g. "Jupyter Notebook,Makefile")'
    )

    return parser.parse_args()

def generator(
    username: str,
    excluded_languages: list[str] | None = None
) -> None:
    print("=" * 45)
    print(" PROFILE ANALYTICS")
    print("=" * 45)

    try:
        # Collect GitHub data
        raw_languages = get_languages(username)

        excluded_languages = excluded_languages or []
        raw_languages = exclude_languages(
            raw_languages,
            excluded_languages
        )

        if excluded_languages:
            print(
                "Excluded languages: "
                + ', '.join(excluded_languages)
            )

        if not raw_languages:
            print("No language data found.")

        # Calculate top 5 languages.
        statistics = calculate_language_percentages(
            raw_languages,
            limit=5
        )

        # Display statistics
        print("\nTOP 5 LANGUAGES\n")

        for language in statistics:
            if language["name"] == "Other":
                continue

            print(
                f"{language['name']:<15}"
                f"{language['percentage']:>8.2f}%"
            )

        # Generate themes
        print("\nRendering SVG cards...\n")

        for theme_name in THEMES:
            render_languages_card(
                statistics,
                theme_name
            )

        print("\nSYSTEM STATUS: CONCLUDED")

    except HTTPError as error:
        print(
            f"GitHub API error: "
            f"{error.code} - {error.reason}"
        )

        if error.code == 403:
            print(
                "Check API rate limits "
                "or authentication."
            )

        raise

    except URLError as error:
        print(f"Network error: {error.reason}")
        raise

    except TimeoutError:
        print("Request timed out.")
        raise

    except Exception as error:
        print(
            f"Unexpected error: "
            f"{type(error).__name__}: {error}"
        )
        raise

if __name__ == "__main__":
    args = parse_args()

    generator(
        args.username,
        [
            name.strip()
            for name in args.exclude_languages.split(',')
            if name.strip()
        ]
    )
