import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\xa0", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_for_matching(text: str) -> str:
    text = clean_text(text)
    text = text.lower()

    replacements = {
        "gcp": "google cloud platform",
        "aws": "amazon web services",
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "ia": "intelligence artificielle",
        "js": "javascript",
    }

    for source, target in replacements.items():
        text = re.sub(rf"\b{re.escape(source)}\b", target, text)

    return text
