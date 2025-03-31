import json
from openai import OpenAI
from django.conf import settings

SYSTEM_PROMPT = """
You are a smart assistant that classifies forest-related questions into one of four categories:

1. Retrieve specific vegetation index averages (e.g.,'NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'SIPI', 'MGRVI', 'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI', 'NDMI', 'MSAVI', 'NDRI', 'RECI' for a given area and time (2020–2025 only).
2. Retrieve burned area mask information for a given area and time (2020–2025 only). If the user does not specify a time range, provide the most recent data within this period.
3. Retrieve forest deforestation mask data for a given area and time (2020–2025 only).
4. Retrieve information about available data in database such as forests, indices, burns and masks.
5. General chat – no database queries.

Available forests and their IDs:
- 1: Semey Ormany
- 2: Semey Ormany 2
- 3: North KZ
- 4: East KZ

Return a JSON with:
- category: 1, 2, 3, 4, or 5
- index: One of the valid indices or null if not applicable
- forest_id: The forest ID from the list above
- start_date: "YYYY-MM-DD" format (start of the period) or "2020-01-01" if not specified
- end_date: "YYYY-MM-DD" format (end of the period) or "2025-12-31" if not specified

Note: Always provide `start_date` and `end_date` even if they are not explicitly mentioned by the user. If not specified, use:
- `start_date`: "2020-01-01"
- `end_date`: "2025-12-31"

Always ensure the dates are within the range from 2020 to 2025. Note that current year is 2025.
"""

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def categorize_question(question: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    print(f"Router: {response}\n")

    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("Categorization failed:", e)
        return {"category": 4}