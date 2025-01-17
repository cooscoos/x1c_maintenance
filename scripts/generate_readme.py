"""Script to generate README file from a maintenance.csv"""

import pandas as pd
from pathlib import Path

# File paths
CSV_FILE = Path.cwd() / 'maintenance.csv'
README_FILE = Path.cwd() / 'README.md'
HEADER_FILE = Path.cwd() / 'scripts' / 'header.md'

# Column to sort the csv by before converting to md table
SORT_BY = 'Freq (non-ABS)'


def csv_to_markdown(csv_path: Path) -> str:
    """Converts a csv to a markdown table using pandas."""
    df = pd.read_csv(csv_path)

    # Create a new column with markdown-formatted links
    df['Maintenance'] = df.apply(
        lambda row: f"[{row['Maintenance']}]({row['Link']})"
            if pd.notna(row['Link']) else row['Maintenance'],
            axis=1
    )

    # Link column not needed in markdown table
    df = df.drop(columns=['Link'])

    # Sort the DataFrame by 'Freq (non-ABS)' column
    df = df.sort_values(by=SORT_BY, ascending=True)

    # Convert DataFrame to Markdown table
    markdown = df.to_markdown(index=False)

    return markdown


def main():
    """Generate README.md from csv file."""
    # Read header text from file
    with open(HEADER_FILE, 'r', encoding='utf-8') as f:
        header_text = f.read()

    markdown_table = csv_to_markdown(CSV_FILE)
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(header_text + "\n\n" + markdown_table)


if __name__ == '__main__':
    main()
