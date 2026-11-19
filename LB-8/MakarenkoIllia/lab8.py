import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_COLS = ("name", "latitude", "longitude")


def load_csv(path):
    good, skipped = [], 0
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            try:
                if None in row or row["latitude"] is None:
                    raise ValueError
                float(row["latitude"])
                float(row["longitude"])
            except (ValueError, TypeError, KeyError):
                skipped += 1
                continue
            good.append(row)
    if skipped:
        print(f"  [{os.path.basename(path)}] пропущено некоректних рядків: {skipped}")
    return good


def make_key(row):
    return (
        row["name"].strip(),
        float(row["latitude"]),
        float(row["longitude"]),
    )


def build_index(rows):
    index = {}
    for row in rows:
        index.setdefault(make_key(row), []).append(row)
    return index

def inner_join(left, right):
    index = build_index(right)
    result = []
    for lrow in left:
        for rrow in index.get(make_key(lrow), ()):
            result.append((lrow, rrow))
    return result


def union(left, right):
    common = ["name", "zipcode", "smart_location", "country", "latitude", "longitude"]
    seen = {}
    result = []
    for source, rows in (("file1", left), ("file2", right)):
        for row in rows:
            key = make_key(row)
            if key in seen:
                if result[seen[key]]["source"] != source:
                    result[seen[key]]["source"] = "both"
                continue
            out = {c: row[c] for c in common}
            out["source"] = source
            seen[key] = len(result)
            result.append(out)
    return result


def not_in(left, right):
    right_keys = set(make_key(r) for r in right)
    return [row for row in left if make_key(row) not in right_keys]

def group_by(rows, key_col, value_cols):
    groups = {}
    for row in rows:
        groups.setdefault(row[key_col], []).append(tuple(row[c] for c in value_cols))
    return groups


def show(title, rows, fmt, limit=5):
    print(f"\n=== {title}: {len(rows)} рядків ===")
    for row in rows[:limit]:
        print("  " + fmt(row))
    if len(rows) > limit:
        print(f"  ... ще {len(rows) - limit}")


def main():
    p1 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "Barcelona1.csv")
    p2 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "Barcelona2.csv")

    f1, f2 = load_csv(p1), load_csv(p2)
    print(f"Barcelona1: {len(f1)} рядків, Barcelona2: {len(f2)} рядків")

    show("JOIN (name+latitude+longitude співпадають)", inner_join(f1, f2),
         lambda p: f"{p[0]['id']} | {p[1]['listing_url']} | {p[0]['name']} | {p[0]['latitude']}, {p[0]['longitude']}")

    uni = union(f1, f2)
    both = sum(1 for r in uni if r["source"] == "both")
    show(f"UNION (з них у обох файлах: {both})", uni,
         lambda r: f"[{r['source']}] {r['name']} | {r['latitude']}, {r['longitude']}")

    show("NOT-IN (є в Barcelona1, немає в Barcelona2)", not_in(f1, f2),
         lambda r: f"{r['id']} | {r['name']} | {r['latitude']}, {r['longitude']}")

    groups = group_by(f1, "zipcode", ("latitude", "longitude"))
    print(f"\n=== GROUP BY zipcode: {len(groups)} груп ===")
    for zipcode in sorted(groups):
        coords = groups[zipcode]
        print(f"zipcode={zipcode or '<порожній>'} ({len(coords)} шт.)")
        for lat, lon in coords:
            print(f"    {lat}, {lon}")


if __name__ == "__main__":
    main()