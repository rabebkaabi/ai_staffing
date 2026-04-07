import csv
import io


def export_candidates_to_csv(rows: list[dict]) -> str:
    output = io.StringIO()

    fieldnames = [
        "nom",
        "prenom",
        "profil",
        "competences",
        "taches",
        "ecarts",
        "score_similarite",
        "rang",
        "decision_ia",
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    return output.getvalue()
