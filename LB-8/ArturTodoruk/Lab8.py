import csv
import sys

KEY_COLS = ("name", "latitude", "longitude")


def load_csv(path):
    rows, skipped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for rec in reader:
            if len(rec) != len(header) or not rec[header.index("latitude")] \
                    or not rec[header.index("longitude")]:
                skipped += 1
                continue
            rows.append(dict(zip(header, rec)))
    if skipped:
        print(f"{path}: пропущено {skipped} пошкоджених рядків")
    return rows


def make_key(row):
    return (row["name"].strip(), float(row["latitude"]), float(row["longitude"]))


def build_index(rows):
    index = {}
    for r in rows:
        index.setdefault(make_key(r), []).append(r)
    return index


def my_join(rows1, rows2):
    index2 = build_index(rows2)
    result = []
    for r1 in rows1:
        for r2 in index2.get(make_key(r1), ()):
            result.append((r1, r2))
    return result


def my_union(rows1, rows2):
    seen = set()
    result = []
    for r in rows1:
        k = make_key(r)
        if k not in seen:
            seen.add(k)
            result.append(r)
    for r in rows2:
        k = make_key(r)
        if k not in seen:
            seen.add(k)
            result.append(r)
    return result


def my_not_in(rows1, rows2):
    keys2 = {make_key(r) for r in rows2}
    return [r for r in rows1 if make_key(r) not in keys2]


def my_group_by_zipcode(rows1):
    groups = {}
    for r in rows1:
        groups.setdefault(r["zipcode"], []).append((r["latitude"], r["longitude"]))
    return groups


def main():
    p1 = sys.argv[1] if len(sys.argv) > 1 else "Barcelona1.csv"
    p2 = sys.argv[2] if len(sys.argv) > 2 else "Barcelona2.csv"
    b1, b2 = load_csv(p1), load_csv(p2)
    print(f"Barcelona1: {len(b1)} рядків, Barcelona2: {len(b2)} рядків\n")

    joined = my_join(b1, b2)
    print(f"JOIN   : {len(joined)} рядків")
    for r1, r2 in joined[:5]:
        print("   ", r1["id"], r2["listing_url"], r1["name"], r1["latitude"], r1["longitude"])

    union = my_union(b1, b2)
    print(f"\nUNION  : {len(union)} рядків")
    for r in union[:5]:
        print("   ", r["name"], r["latitude"], r["longitude"])

    not_in = my_not_in(b1, b2)
    print(f"\nNOT-IN : {len(not_in)} рядків")
    for r in not_in[:5]:
        print("   ", r["id"], r["name"], r["latitude"], r["longitude"])

    groups = my_group_by_zipcode(b1)
    print(f"\nGROUP BY zipcode: {len(groups)} груп")
    for zipcode in sorted(groups)[:5]:
        coords = groups[zipcode]
        print(f"   zipcode={zipcode} ({len(coords)} шт.)")
        for lat, lon in coords[:3]:
            print(f"      {lat}, {lon}")
        if len(coords) > 3:
            print("      ...")


if __name__ == "__main__":
    main()