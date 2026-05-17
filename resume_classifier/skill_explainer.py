import re


CATEGORY_SKILLS = {
    "Python Developer": [
        "python", "django", "flask", "fastapi", "rest api", "api",
        "sql", "mysql", "postgresql", "git", "github", "docker",
        "aws", "linux", "testing", "debugging", "oop",
        "data structures", "algorithms"
    ],

    "Java Developer": [
        "java", "spring", "spring boot", "hibernate", "maven",
        "sql", "mysql", "postgresql", "rest api", "api",
        "git", "docker", "aws", "testing", "oop"
    ],

    "Database": [
        "sql", "mysql", "postgresql", "oracle", "mariadb",
        "database", "backup", "recovery", "replication",
        "indexing", "query optimization", "stored procedure",
        "performance tuning", "security"
    ],

    "Web Designing": [
        "html", "css", "javascript", "bootstrap", "jquery",
        "react", "ui", "ux", "responsive design", "wordpress"
    ],
    "Sales": [
        "sales",
        "customer service",
        "lead generation",
        "prospecting",
        "cold calling",
        "client relationship",
        "account management",
        "crm",
        "salesforce",
        "negotiation",
        "closing",
        "quota",
        "revenue",
        "business development",
        "presentation",
        "communication",
        "market research",
        "pipeline",
        "customer retention",
    ],
}


DEFAULT_SKILLS = [
    "python", "sql", "mysql", "api", "git", "docker",
    "javascript", "html", "css", "linux", "testing", "debugging"
]


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_skill_list_for_category(predicted_category):
    predicted_category = str(predicted_category)

    if predicted_category in CATEGORY_SKILLS:
        return CATEGORY_SKILLS[predicted_category]

    for category, skills in CATEGORY_SKILLS.items():
        if category.lower() in predicted_category.lower():
            return skills

    return DEFAULT_SKILLS


def explain_skills(resume_text, predicted_category):
    cleaned = clean_text(resume_text)
    expected_skills = get_skill_list_for_category(predicted_category)

    matched_skills = [
        skill for skill in expected_skills
        if skill.lower() in cleaned
    ]

    missing_skills = [
        skill for skill in expected_skills
        if skill.lower() not in cleaned
    ]

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_count": len(matched_skills),
        "total_skills": len(expected_skills),
    }