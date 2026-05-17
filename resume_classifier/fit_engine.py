def normalize_text(value):
    return str(value or "").lower().strip()


def decide_fit(predicted_category, category_confidence, position_applied):
    predicted = normalize_text(predicted_category)
    applied = normalize_text(position_applied)

    category_matches = (
        predicted in applied
        or applied in predicted
        or any(word in predicted for word in applied.split())
    )

    if category_matches and category_confidence >= 0.10:
        fit_label = "Strong Candidate"
        explanation = (
            f"The resume category '{predicted_category}' matches the applied position "
            f"'{position_applied}', so the candidate is considered a strong fit."
        )
    elif category_matches:
        fit_label = "Needs Review"
        explanation = (
            f"The resume category '{predicted_category}' appears related to the applied position "
            f"'{position_applied}', but the model confidence is low."
        )
    else:
        fit_label = "Not a Fit"
        explanation = (
            f"The resume category '{predicted_category}' does not clearly match the applied position "
            f"'{position_applied}'."
        )

    return {
        "fit_label": fit_label,
        "fit_explanation": explanation,
    }