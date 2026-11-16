import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_csv(filename):
    filepath = os.path.join(BASE_DIR, filename)
    rows = []
    with open(filepath, mode="r", encoding="utf-8", errors="replace", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("name") and row.get("latitude") and row.get("longitude"):
                rows.append(row)
    return rows


def get_key(row):
    name = (row.get("name") or "").strip()
    lat = (row.get("latitude") or "").strip()
    lon = (row.get("longitude") or "").strip()

    if not name or not lat or not lon:
        return None

    try:
        return (name, round(float(lat), 6), round(float(lon), 6))
    except ValueError:
        return (name, lat, lon)


def custom_join(data1, data2):
    index2 = {}
    for row in data2:
        key = get_key(row)
        if key:
            index2.setdefault(key, []).append(row)

    result = []
    for row1 in data1:
        key = get_key(row1)
        if key in index2:
            for row2 in index2[key]:
                merged = {
                    "id": row1.get("id", ""),
                    "listing_url": row2.get("listing_url", ""),
                    "name": row1.get("name", ""),
                    "zipcode": row1.get("zipcode") or row2.get("zipcode", ""),
                    "smart_location": row1.get("smart_location", ""),
                    "country": row1.get("country", ""),
                    "latitude": row1.get("latitude", ""),
                    "longitude": row1.get("longitude", ""),
                }
                result.append(merged)
    return result


def custom_union(data1, data2):
    seen = set()
    result = []

    for row in data1:
        key = get_key(row)
        if key and key not in seen:
            seen.add(key)
            result.append(row)

    for row in data2:
        key = get_key(row)
        if key and key not in seen:
            seen.add(key)
            result.append(row)

    return result


def custom_not_in(data1, data2):
    keys2 = set()
    for row in data2:
        key = get_key(row)
        if key:
            keys2.add(key)

    result = []
    for row1 in data1:
        key = get_key(row1)
        if key and key not in keys2:
            result.append(row1)

    return result


if __name__ == "__main__":
    barcelona1 = load_csv("Barcelona1.csv")
    barcelona2 = load_csv("Barcelona2.csv")

    join_rows = custom_join(barcelona1, barcelona2)
    union_rows = custom_union(barcelona1, barcelona2)
    not_in_rows = custom_not_in(barcelona1, barcelona2)

    print(f"JOIN (збіги у двох файлах): {len(join_rows)}")
    for r in join_rows[:5]:
        print(r)

    print(f"\nUNION (усі унікальні рядки): {len(union_rows)}")
    for r in union_rows[:5]:
        print(r)

    print(f"\nNOT-IN (є в Barcelona1, немає в Barcelona2): {len(not_in_rows)}")
    for r in not_in_rows[:5]:
        print(r)