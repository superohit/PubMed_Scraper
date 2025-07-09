import re


def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university",
        "college",
        "institute",
        "school",
        "hospital",
        "center",
    ]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)


def extract_company_name(affiliation: str) -> str:
    match = re.search(
        r"([A-Z][\w&,\s]+(?:Inc\.|Ltd\.|LLC|Pharma|Biotech|Corporation))", affiliation
    )
    return match.group(1) if match else ""


def extract_email(affiliation: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", affiliation)
    return match.group(0) if match else ""
