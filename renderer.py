from pathlib import Path
from math import ceil
from xml.sax.saxutils import escape
from consts import THEMES

OUTPUT_DIR = Path("output")

def render_languages_card(
    languages: list,
    theme_name: str
) -> None:
    theme = THEMES[theme_name]

    width = 600
    padding = 22
    columns = 2

    rows = ceil(len(languages) / columns)

    height = max(220, 172 + rows * 27)

    elements = []

    def add(value):
        elements.append(value)

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    add(f"""
    <rect width="{width}" height="{height}"
          fill="{theme['bg']}"
          stroke="{theme['border']}"/>
    """)

    # --------------------------------------------------------
    # TEXTURES
    # --------------------------------------------------------

    add(f"""
    <defs>

      <pattern id="grid" width="18" height="18"
               patternUnits="userSpaceOnUse">

        <path d="M 18 0 L 0 0 0 18"
              fill="none"
              stroke="{theme['grid']}"
              stroke-width="0.5"/>

      </pattern>

      <pattern id="dots" width="9" height="9"
               patternUnits="userSpaceOnUse">

        <circle cx="1" cy="1" r="0.6"
                fill="{theme['secondary']}"/>

      </pattern>

      <clipPath id="bar-clip">

        <rect x="{padding}" y="112"
              width="{width - padding * 2}"
              height="16"/>

      </clipPath>

    </defs>

    <rect width="{width}" height="{height}"
          fill="url(#grid)" opacity="0.32"/>

    <rect width="{width}" height="{height}"
          fill="url(#dots)" opacity="0.12"/>
    """)

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    add(f"""
    <text x="{padding}" y="19"
          fill="{theme['secondary']}"
          font-family="monospace"
          font-size="9">

      ▦ MAP   ▦ QUESTS   ▦ ITEMS   ▦ SYSTEM

    </text>

    <text x="{width-padding}" y="19"
          text-anchor="end"
          fill="{theme['accent']}"
          font-family="monospace"
          font-size="9">

      UNIT 01

    </text>
    """)

    add(f"""
    <line x1="{padding}" y1="29"
          x2="{width-padding}" y2="29"
          stroke="{theme['border']}"/>
    """)

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    add(f"""
    <text x="{padding}" y="61"
          fill="{theme['fg']}"
          font-family="monospace"
          font-size="25"
          font-weight="bold">

      Programming Languages

    </text>
    """)

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    add(f"""
    <text x="{padding}" y="91"
          fill="{theme['secondary']}"
          font-family="monospace"
          font-size="9">

      ↑ SORT: USAGE

    </text>

    <text x="{width-padding}" y="91"
          text-anchor="end"
          fill="{theme['secondary']}"
          font-family="monospace"
          font-size="9">

      STATUS: VERIFIED

    </text>
    """)

    # --------------------------------------------------------
    # LANGUAGE BAR
    # --------------------------------------------------------

    bar_x = padding
    bar_y = 112
    bar_width = width - padding * 2

    add(f"""
    <rect x="{bar_x}" y="{bar_y}"
          width="{bar_width}" height="16"
          fill="{theme['bar_bg']}"/>
    """)

    current_x = bar_x

    for language in languages:
        percentage = language["percentage"]
        segment_width = bar_width * percentage / 100
        color = language["color"]

        if segment_width > 0:
            add(f"""
            <rect x="{current_x:.3f}" y="{bar_y}"
                  width="{segment_width:.3f}"
                  height="16"
                  fill="{color}"
                  clip-path="url(#bar-clip)"/>
            """)

        current_x += segment_width

    # --------------------------------------------------------
    # LANGUAGE LEGEND
    # --------------------------------------------------------

    legend_y = 158
    column_width = bar_width / columns

    for index, language in enumerate(languages):
        column = index % columns
        row = index // columns
        x = padding + column * column_width
        y = legend_y + row * 27

        name = escape(language["name"])
        percentage = language["percentage"]
        color = language["color"]

        add(f"""
        <rect x="{x}" y="{y-10}"
              width="11" height="11"
              fill="{color}"/>

        <text x="{x+18}" y="{y}"
              fill="{theme['fg']}"
              font-family="monospace"
              font-size="11">

          {name} {percentage:.2f}%

        </text>
        """)

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer_y = height - 13

    add(f"""
    <line x1="{padding}" y1="{footer_y-17}"
          x2="{width-padding}" y2="{footer_y-17}"
          stroke="{theme['border']}"/>

    <text x="{padding}" y="{footer_y}"
          fill="{theme['accent']}"
          font-family="monospace"
          font-size="9">

      NO ERROR

    </text>

    <text x="{width-padding}" y="{footer_y}"
          text-anchor="end"
          fill="{theme['secondary']}"
          font-family="monospace"
          font-size="9">

      YORHA SYSTEM // 01

    </text>
    """)

    # --------------------------------------------------------
    # SVG DOCUMENT
    # --------------------------------------------------------

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}"
         height="{height}"
         viewBox="0 0 {width} {height}">

      {''.join(elements)}

    </svg>
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        OUTPUT_DIR /
        f"languages-{theme_name}.svg"
    )

    filename.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Generated: {filename}")
