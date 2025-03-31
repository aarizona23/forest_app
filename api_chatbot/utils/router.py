import json
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def categorize_question(question: str) -> dict:
    SYSTEM_PROMPT = """
You are a smart assistant that classifies forest-related questions into one of four categories:

1. Retrieve specific vegetation index averages (e.g., NDVI, EVI, NDWI, NBR, SAVI, GNDVI, NDRE, SIPI, MGRVI, TGI, VARI, GRVI, SR, CI, MSR, OSAVI, NDMI, MSAVI, NDRI, RECI) for a given area and time (2020–2025 only).
2. Retrieve burned area mask information for a given area and time (2020–2025 only). If the user does not specify a time range, provide the most recent data within this period.
3. Retrieve forest reclassification (reforestation) mask data for a given area and time (2020–2025 only).
4. General chat – no database queries.

Available forests and their IDs:
- 1: Semey Ormany
- 2: Semey Ormany 2
- 3: North KZ
- 4: East KZ

Return a JSON with:
- category: 1, 2, 3, or 4
- index: One of the valid indices or null if not applicable
- forest_id: The forest ID from the list above
- start_date: "YYYY-MM-DD" format (start of the period) or null (If not specified, use "2020-01-01")
- end_date: "YYYY-MM-DD" format (end of the period) or null (If not specified, use "2025-12-31")

Always return start_date and end_date within the range from 2020 to 2025.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    print("Router: ", response)

    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("Categorization failed:", e)
        return {"category": 4}