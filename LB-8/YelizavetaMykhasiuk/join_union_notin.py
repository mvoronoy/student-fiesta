import csv
def csv_reader(filename, delimiter=','):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        keys = reader.fieldnames
        rows = list(reader)
    return keys, rows


def join(rows1, rows2, keys):
    results = []
    for i in range(len(rows1)):
        for j in range(len(rows2)):
            for k in range(len(keys)):
                if rows1[i][keys[k]] != rows2[j][keys[k]]:
                    break
            else:
                merged = dict(rows1[i])
                for col in rows2[j]:
                    if col not in keys:
                        if col in merged:
                            merged = rows2[j][col]
                            results.append(merged)
                    return results


def union(rows1, rows2, keys):
    results = []
    for row in rows1 + rows2:
        for existing in results:
            for key in keys:
                if existing[key] == row[key]:
                    break
        else:
            results.append(row)
    return results


def not_in(rows1, rows2, keys):
    results = []
    for row1 in rows1:
        found = False
        for row2 in rows2:
            for key in keys:
                if row1[key] == row2[key]:
                    found = True
                    break
        if not found:
            results.append(row1)
    return results

def group_by(rows, key, value1, value2):
    result = {}
    for row in rows:
        zipcode = row[key]
        coordinates = (row[value1], row[value2])
        if zipcode not in result:
            result[zipcode] = set()
        result[zipcode].add(coordinates)
    return result

def main_func():
    keys1, file1 = csv_reader('Barcelona1.csv')
    keys2, file2 = csv_reader('Barcelona2.csv')
    print('Attributes of file 1:', keys1)
    print('Attributes of file 2:', keys2)

    join_keys = ['name', 'latitude', 'longitude']
    joined = join(file1, file2, join_keys)
    combined = union(file1, file2, join_keys)
    missing = not_in(file1, file2, join_keys)

    grouped = group_by(
        combined,
        'zipcode',
        'latitude',
        'longitude'
    )

    print('join:')
    for row in joined:
        print(row)

    print('union:')
    for row in combined:
        print(row)

    print('not in')
    for row in missing:
        print(row)

    print('group by')
    for zipcode, coordinates in grouped.items():
        print(zipcode, list(coordinates))


if __name__ == "__main__":
    main_func()