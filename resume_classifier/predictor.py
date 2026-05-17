from pathlib import Path
import re
import joblib


BASE_DIR = Path(__file__).resolve().parent

CATEGORY_MODEL_PATH = BASE_DIR / "ml_artifacts" / "resume_category_model.pkl"
CATEGORY_VECTORIZER_PATH = BASE_DIR / "ml_artifacts" / "resume_category_vectorizer.pkl"


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_category_artifacts():
    model = joblib.load(CATEGORY_MODEL_PATH)
    vectorizer = joblib.load(CATEGORY_VECTORIZER_PATH)
    return model, vectorizer


def predict_resume_category(resume_text: str):
    model, vectorizer = load_category_artifacts()

    cleaned_text = clean_text(resume_text)
    vectorized_text = vectorizer.transform([cleaned_text])

    predicted_category = model.predict(vectorized_text)[0]

    top_categories = []

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(vectorized_text)[0]
        classes = model.classes_

        top_indices = probabilities.argsort()[-1:][::-1]

        top_categories = [
            {
                "category": classes[index],
                "confidence": float(probabilities[index]),
            }
            for index in top_indices
        ]

        category_confidence = float(probabilities.max())
    else:
        category_confidence = None

    return {
        "predicted_category": predicted_category,
        "category_confidence": category_confidence,
        "top_categories": top_categories,
    }