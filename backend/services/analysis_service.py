from services.gemini_service import generate_response
import json


def analyze_report(report_text):

    prompt = """
You are an experienced clinical document analysis assistant.

Analyze the medical report carefully.

Return ONLY valid JSON.

The summary should:
- Be 3-5 sentences.
- Mention ONLY the important medical findings.
- Mention abnormal values if present.
- If all values are normal, clearly state that.
- Do not contradict yourself.
- Do not invent diseases.
- Do not repeat the report word-for-word.

The risk assessment should:
- Explain why the report is Low, Moderate, or High risk.
- Base the decision only on the report.

Recommendations:
- Give practical next steps.
- If everything is normal, recommend routine follow-up only.

Return exactly:

{
  "report_type": "",
  "summary": "",
  "key_findings": [],
  "abnormal_findings": [],
  "risk_level": "",
  "risk_assessment": "",
  "recommendations": [],
  "follow_up_tests": []
}
"""

    response = generate_response(
        report_text,
        prompt
    )

    try:

        # Extract JSON if extra text exists
        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON found")

        json_string = response[start:end + 1]

        data = json.loads(json_string)

        return {

            "report_type": data.get("report_type", ""),

            "summary": data.get("summary", ""),

            "key_findings": data.get("key_findings", []),

            "abnormal_findings": data.get("abnormal_findings", []),

            "risk_level": data.get("risk_level", "Unknown"),

            "risk_assessment": data.get("risk_assessment", ""),

            "recommendations": data.get("recommendations", []),

            "follow_up_tests": data.get("follow_up_tests", [])

        }

    except Exception as e:

        print("JSON Parsing Error:", e)
        print(response)

        return {

            "report_type": "",

            "summary": "",

            "key_findings": [],

            "abnormal_findings": [],

            "risk_level": "Unknown",

            "risk_assessment": "",

            "recommendations": [],

            "follow_up_tests": []

        }