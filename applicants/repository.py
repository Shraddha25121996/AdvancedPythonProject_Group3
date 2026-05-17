from django.db import connection


def dict_fetch_all(cursor):
    columns = [column[0] for column in cursor.description]

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_all_applicants():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                position_applied,
                status,
                notes,
                created_at,
                resume_file,
                resume_prediction,
                resume_confidence,
                resume_classified_at
            FROM applicants
            ORDER BY created_at DESC
        """)

        return dict_fetch_all(cursor)


def create_applicant(data):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO applicants (
                first_name,
                last_name,
                email,
                phone,
                position_applied,
                status,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, [
            data["first_name"],
            data["last_name"],
            data["email"],
            data.get("phone"),
            data["position_applied"],
            data["status"],
            data.get("notes"),
        ])

def count_applicants():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM applicants
        """)

        row = cursor.fetchone()

        return row[0] if row else 0
    

def get_applicant_by_id(applicant_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                position_applied,
                status,
                notes,
                created_at,
                resume_file,
                resume_prediction,
                resume_confidence,
                resume_explanation,
                top_categories_json,
                fit_label,
                fit_explanation,
                matched_skills_json,
                missing_skills_json,
                resume_classified_at
            FROM applicants
            WHERE id = %s
        """, [applicant_id])

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))


def update_applicant(applicant_id, data):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE applicants
            SET
                first_name = %s,
                last_name = %s,
                email = %s,
                phone = %s,
                position_applied = %s,
                status = %s,
                notes = %s
            WHERE id = %s
        """, [
            data["first_name"],
            data["last_name"],
            data["email"],
            data.get("phone"),
            data["position_applied"],
            data["status"],
            data.get("notes"),
            applicant_id,
        ])  

def update_applicant_resume(applicant_id, resume_file):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE applicants
            SET resume_file = %s
            WHERE id = %s
        """, [resume_file, applicant_id])


def update_applicant_classification(
    applicant_id,
    prediction,
    confidence,
    classified_at,
    explanation=None,
    top_categories_json=None,
    fit_label=None,
    fit_explanation=None,
    matched_skills_json=None,
    missing_skills_json=None,
):
    with connection.cursor() as cursor:
        cursor.execute("""
    UPDATE applicants
    SET
        resume_prediction = %s,
        resume_confidence = %s,
        resume_classified_at = %s,
        resume_explanation = %s,
        top_categories_json = %s,
        fit_label = %s,
        fit_explanation = %s,
        matched_skills_json = %s,
        missing_skills_json = %s
    WHERE id = %s
""", [
    prediction,
    confidence,
    classified_at,
    explanation,
    top_categories_json,
    fit_label,
    fit_explanation,
    matched_skills_json,
    missing_skills_json,
    applicant_id,
])