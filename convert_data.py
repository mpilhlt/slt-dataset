"""
Convert the raw Excel survey file to a CSV with SQL-safe column names.

Usage:
    uv run python convert_data.py

Outputs:
    data/slt_raw_data.csv        — survey data with sanitized column names
    data/slt_column_mapping.csv  — maps sanitized names back to original questions
"""

import re
import pandas as pd

EXCEL_FILE  = "data/results-for-socio-legal-t-2021-12-14-1607.xlsx"
SHEET_NAME  = "Raw data"
CSV_OUT     = "data/slt_raw_data.csv"
MAPPING_OUT = "data/slt_column_mapping.csv"


def sanitize_column(col: str) -> str:
    """Turn a survey question string into a valid SQL/Python identifier.

    '2. Which academic community are you part of?' → 'q2_which_academic_community_are'
    '14.b.ii.1.a. Teaching (including student mentoring)' → 'q14_b_ii_1_a_teaching_including_student'
    """
    m = re.match(r'^([\d]+(?:[.\w]+)?\.)\s*', col)
    if m:
        prefix = re.sub(r'[^a-z0-9]', '_', m.group(1).lower()).strip('_')
        rest = col[m.end():].strip()
    else:
        prefix = ''
        rest = col.strip()

    words = re.sub(r'[^a-zA-Z0-9 ]', ' ', rest).split()[:5]
    suffix = '_'.join(w.lower() for w in words if w)
    name = f"q{prefix}_{suffix}" if prefix else suffix
    return re.sub(r'_+', '_', name).strip('_')[:60]


def build_rename_map(columns: list[str]) -> dict[str, str]:
    seen: dict[str, int] = {}
    mapping: dict[str, str] = {}
    for orig in columns:
        base = sanitize_column(orig)
        seen[base] = seen.get(base, 0) + 1
        mapping[orig] = f"{base}_{seen[base]}" if seen[base] > 1 else base
    return mapping


def main() -> None:
    print(f"Reading '{EXCEL_FILE}' sheet '{SHEET_NAME}' …")
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    rename_map = build_rename_map(list(df.columns))
    df = df.rename(columns=rename_map)

    df.to_csv(CSV_OUT, index=False)
    print(f"Wrote {len(df):,} rows x {len(df.columns)} columns -> {CSV_OUT}")

    mapping_df = pd.DataFrame(
        {"column": list(rename_map.values()), "original_question": list(rename_map.keys())}
    )
    mapping_df.to_csv(MAPPING_OUT, index=False)
    print(f"Wrote column mapping -> {MAPPING_OUT}")


if __name__ == "__main__":
    main()
