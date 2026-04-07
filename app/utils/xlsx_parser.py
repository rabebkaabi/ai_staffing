import pandas as pd


def parse_xlsx(file_path: str) -> str:
    excel_file = pd.ExcelFile(file_path)
    sheet_texts = []

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        if not df.empty:
            sheet_text = df.fillna("").astype(str).to_string(index=False)
            sheet_texts.append(f"[SHEET: {sheet_name}]\n{sheet_text}")

    return "\n\n".join(sheet_texts).strip()
