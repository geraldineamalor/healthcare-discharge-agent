import textstat

def get_readability(text):
    return {
        "Grade Level": textstat.flesch_kincaid_grade(text),
        "Reading Ease": textstat.flesch_reading_ease(text)
    }
