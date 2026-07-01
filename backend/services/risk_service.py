from services.gemini_service import generate_response


def generate_risk_prediction(report_text):

    prompt = """
You are an AI medical report analyzer.

Analyze the report and return ONLY in this format.

Risk Level:
Low / Moderate / High

Risk Assessment:
A short explanation of why the patient falls into this risk category.

Recommendations:
Provide 2-3 short recommendations.

Do not diagnose diseases.

Do not include markdown.

Do not include any extra headings.

End with:
Disclaimer:
This is AI-generated and should not replace professional medical advice.
"""

    response = generate_response(
        report_text,
        prompt
    )

    risk_level = "Unknown"

    risk_assessment = response

    if "Risk Level:" in response:

        try:

            risk_level = (
                response
                .split("Risk Level:")[1]
                .split("\n")[0]
                .strip()
            )

        except:

            pass

    return {

        "risk_level": risk_level,

        "risk_assessment": risk_assessment

    }