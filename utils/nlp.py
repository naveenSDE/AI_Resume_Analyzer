import spacy

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


def extract_skills(text):
    """
    Extracts potential skills from text using NER and simple rule-based matching.
    Note: A production system would use a dedicated skills database or more advanced patterns.
    For this MVP, we'll use Noun Chunks and Entities to approximate skills.
    """
    doc = nlp(text)
    skills = set()

    # Extract entities that might be skills (ORG, PRODUCT, LANGUAGE, GPE for location based skills?)
    # This is a simplification.
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "LANGUAGE", "WORK_OF_ART"]:
            skills.add(ent.text.lower())

    # Also look for noun chunks that are often skills
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Short phrases
            skills.add(chunk.text.lower())

    return skills


def analyze_resume(resume_text, job_description):
    """
    Analyzes the resume against the job description.
    """
    resume_doc = nlp(resume_text)
    jd_doc = nlp(job_description)

    # 1. Calculate Similarity Score
    # spaCy's similarity needs vectors. en_core_web_sm doesn't have vectors,
    # so it uses context-sensitive tensors. It's okay for MVP but 'en_core_web_md' is better.
    # We will use a set-based similarity for skills as a fallback/augment.

    similarity_score = resume_doc.similarity(jd_doc)
    match_score = round(similarity_score * 100, 2)

    # 2. Extract Skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # 3. Find Matched and Missing Skills
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)

    # 4. Generate Suggestions
    suggestions = []
    if match_score < 50:
        suggestions.append(
            "Your resume has a low match score. Try to incorporate more keywords from the job description.")
    if len(missing_skills) > 0:
        suggestions.append(f"Consider adding these missing skills: {', '.join(list(missing_skills)[:5])}...")
    if len(resume_text.split()) < 200:
        suggestions.append("Your resume seems a bit short. Elaborate on your experience.")

    return {
        "match_score": match_score,
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "suggestions": suggestions,
        "resume_summary": resume_text[:500] + "..."  # Preview
    }
