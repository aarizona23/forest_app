from api_forest.models import ForestModel, IndicesModel, BurnedMaskModel, ForestMaskModel
from datetime import datetime

ALLOWED_AREAS = [
    "North Kazakhstan", "Semey Ormany", "Jetisu", "East Kazakhstan"
]

def get_index_summary(parsed: dict) -> str:
    area = parsed.get("area")
    index = parsed.get("index")
    start = max(parsed.get("start_year") or 2020, 2020)
    end = min(parsed.get("end_year") or 2025, 2025)

    if area not in ALLOWED_AREAS:
        return f"Area '{area}' is not supported."

    forest = ForestModel.objects.filter(name__icontains=area).first()
    if not forest:
        return f"No data found for {area}"

    entries = IndicesModel.objects.filter(
        forest=forest, name=index,
        timestamp__year__gte=start,
        timestamp__year__lte=end
    ).order_by("timestamp")

    if not entries.exists():
        return f"No {index} data found for {area} between {start}-{end}"

    year_data = {}
    for e in entries:
        year = e.timestamp.year
        year_data.setdefault(year, []).append(e.value)

    summary = f"{index} yearly averages for {area}:\n"
    for year in sorted(year_data):
        avg = sum(year_data[year]) / len(year_data[year])
        summary += f"• {year}: {avg:.2f}\n"

    return summary


def get_burned_area_summary(parsed: dict) -> str:
    area = parsed.get("area")
    start = parsed.get("start_year") or 2020
    end = parsed.get("end_year") or 2025

    forest = ForestModel.objects.filter(name__icontains=area).first()
    if not forest:
        return f"No burned area data for {area}"

    entries = BurnedMaskModel.objects.filter(
        forest=forest,
        timestamp__year__gte=start,
        timestamp__year__lte=end
    )

    return f"{entries.count()} burned mask images found for {area} ({start}–{end})"


def get_deforestation_summary(parsed: dict) -> str:
    area = parsed.get("area")
    start = parsed.get("start_year") or 2020
    end = parsed.get("end_year") or 2025

    forest = ForestModel.objects.filter(name__icontains=area).first()
    if not forest:
        return f"No forest mask data for {area}"

    entries = ForestMaskModel.objects.filter(
        forest=forest,
        timestamp__year__gte=start,
        timestamp__year__lte=end
    )

    return f"{entries.count()} forest classification masks found for {area} ({start}–{end})"
