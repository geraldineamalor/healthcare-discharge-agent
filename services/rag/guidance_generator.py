def extract_section(content, header):
    if header not in content:
        return []
    section = content.split(header)[1]
    lines = []
    for line in section.splitlines():
        if line.startswith("-"):
            lines.append(line.strip("- ").strip())
        elif line.strip() == "":
            break
    return lines


# services/rag/guidance_generator.py

def generate_guidance(retrieved_docs):
    care_guidance = []
    lifestyle_guidance = []

    for doc in retrieved_docs:
        if not isinstance(doc, dict):
            continue

        text = doc.get("content", "").lower()

        if "medication" in text or "take" in text:
            care_guidance.append("Follow prescribed medications exactly as directed.")

        if "avoid" in text or "exercise" in text or "activity" in text:
            lifestyle_guidance.append("Avoid strenuous activity and follow lifestyle advice.")

    return list(set(care_guidance)), list(set(lifestyle_guidance))
