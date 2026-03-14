def route_question(question):

    q = question.lower()

    csv_keywords = [
        "risk",
        "score",
        "inspection",
        "permits",
        "trir",
        "dart",
        "training",
        "compliance"
    ]

    txt_keywords = [
        "owner",
        "overview",
        "fields",
        "who",
        "related"
    ]

    if any(word in q for word in csv_keywords) and any(word in q for word in txt_keywords):
        return "HYBRID"

    if any(word in q for word in csv_keywords):
        return "CSV"

    return "TXT"