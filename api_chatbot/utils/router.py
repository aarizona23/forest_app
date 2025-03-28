import json
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def categorize_question(question: str) -> dict:
    SYSTEM_PROMPT = """
    You are a smart assistant that classifies forest-related user questions into one of four categories:

    1. Retrieve vegetation index averages (e.g., NDVI, EVI, SAVI) for a specific area and time period.
    2. Retrieve burned area mask information.
    3. Retrieve forest reclassification (deforestation) mask information.
    4. General knowledge questions (no database access required).

    Instructions:
    - Always choose the **most relevant vegetation index** for category 1.
    - If the user says "vegetation", "green cover", or "plant health", use "NDVI".
    - If the user mentions fire, burnt area, damage, or smoke, choose category 2.
    - If the user asks about regrowth, reforestation, recovery, or land cover classification, choose category 3.
    - For vague or general questions (like "What is NDVI?"), choose category 4.

    Accepted areas: "North Kazakhstan", "Semey Ormany", "Jetisu", "East Kazakhstan".
    Time period must be between 2020 and 2025.

    Return a valid JSON with:
    - category: 1, 2, 3, or 4
    - index: 'NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'NDRE', 'SIPI', 'MGRVI',
        'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI', 'NDMI', 'MSAVI', 'NDRI', 'RECI'(for category 1 only; null otherwise)
    - area: one of the allowed areas or null
    - start_year: year from 2020–2025 or null
    - end_year: year from 2020–2025 or null

    Example Output:
    {
    "category": 1,
    "index": "NDVI",
    "area": "Semey Ormany",
    "start_year": 2021,
    "end_year": 2023
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0,
        response_format = {"type": "json_object"}
    )

    print("Router: ", response)

    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("Categorization failed:", e)
        return {"category": 4}
