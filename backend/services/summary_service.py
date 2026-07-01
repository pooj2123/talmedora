from services.gemini_service import generate_response


def generate_report_summary(report_text):

    prompt = """
You are a medical report summarization assistant.

Generate a concise summary in the following format:

Report Overview:
(1-2 sentences)

Key Findings:
- ...
- ...

Abnormal Findings:
- ...

Recommendations:
- ...

Disclaimer:
This summary is AI-generated and should not replace professional medical advice.
"""

    return generate_response(report_text, prompt)