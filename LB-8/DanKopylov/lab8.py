import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_csv(filename):
    rows = []

    path = BASE_DIR / filename

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def clean(value):
    if value is None:
        return ""

    return str(value).strip()


def make_key(row):
    return (
        clean(row.get("name")),
        clean(row.get("latitude")),
        clean(row.get("longitude"))
    )


# Аналог JOIN
def custom_join(file1, file2):
    file2_index = {}

    for row in file2:
        key = make_key(row)

        if key not in file2_index:
            file2_index[key] = row

    result = []

    for row in file1:
        key = make_key(row)

        if key in file2_index:
            result.append(row)

    return result


# Аналог UNION
def custom_union(file1, file2):
    result = []
    used_keys = set()

    for row in file1:
        key = make_key(row)

        if key not in used_keys:
            used_keys.add(key)
            result.append(row)

    for row in file2:
        key = make_key(row)

        if key not in used_keys:
            used_keys.add(key)
            result.append(row)

    return result


# Аналог NOT IN
def custom_not_in(file1, file2):
    file2_keys = set()

    for row in file2:
        file2_keys.add(make_key(row))

    result = []

    for row in file1:
        if make_key(row) not in file2_keys:
            result.append(row)

    return result


# Аналог GROUP BY
def custom_group_by(file1):
    groups = {}

    for row in file1:
        zipcode = clean(row.get("zipcode"))

        if not zipcode:
            zipcode = "No_Zip"

        latitude = clean(row.get("latitude"))
        longitude = clean(row.get("longitude"))

        if zipcode not in groups:
            groups[zipcode] = []

        groups[zipcode].append(
            (latitude, longitude)
        )

    return groups


def print_examples(title, rows, count=5):
    print(f"\n=== {title} ===")
    print(f"Кількість записів: {len(rows)}")

    for row in rows[:count]:
        print(
            row.get("name"),
            "|",
            row.get("latitude"),
            "|",
            row.get("longitude")
        )


def main():
    barcelona1 = load_csv("Barcelona1.csv")
    barcelona2 = load_csv("Barcelona2.csv")

    print("Barcelona1:", len(barcelona1), "рядків")
    print("Barcelona2:", len(barcelona2), "рядків")

    join_result = custom_join(barcelona1, barcelona2)
    union_result = custom_union(barcelona1, barcelona2)
    not_in_result = custom_not_in(barcelona1, barcelona2)

    print_examples("JOIN", join_result)
    print_examples("UNION", union_result)
    print_examples("NOT IN", not_in_result)

    groups = custom_group_by(barcelona1)

    print("\n=== GROUP BY zipcode ===")
    print("Кількість груп:", len(groups))

    shown = 0

    for zipcode, coordinates in groups.items():
        print(f"\nZipcode: {zipcode}")

        for latitude, longitude in coordinates[:3]:
            print(f"  {latitude}, {longitude}")

        shown += 1

        if shown == 5:
            break


if __name__ == "__main__":
    main()