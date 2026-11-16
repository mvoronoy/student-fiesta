import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def custom_group_by(filename):
    filepath = os.path.join(BASE_DIR, filename)
    groups = {}

    with open(filepath, mode="r", encoding="utf-8", errors="replace", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = (row.get("latitude") or "").strip()
            lon = (row.get("longitude") or "").strip()

            if not lat or not lon:
                continue

            zipcode = (row.get("zipcode") or "").strip() or "Без індексу"

            if zipcode not in groups:
                groups[zipcode] = []

            groups[zipcode].append((lat, lon))

    return groups


if __name__ == "__main__":
    grouped = custom_group_by("Barcelona1.csv")

    for zipcode, coords in grouped.items():
        print(f"Zipcode: {zipcode}")
        for lat, lon in coords:
            print(f"   latitude: {lat}, longitude: {lon}")