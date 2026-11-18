import csv

def load_csv(filename):
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Попередження: файл {filename} не знайдено.")
    return data

def main():
    file1 = load_csv('Barcelona1.csv')
    file2 = load_csv('Barcelona2.csv')

    if not file1 or not file2:
        print("Помилка: перевір, чи лежать Barcelona1.csv та Barcelona2.csv у цій самій папці.")
        return

    def get_key(row):
        lat = row.get('latitude')
        lon = row.get('longitude')
        zip_c = row.get('zipcode')

        return (
            str(zip_c).strip() if zip_c is not None else '',
            str(lat).strip() if lat is not None else '',
            str(lon).strip() if lon is not None else ''
        )

    set2 = {get_key(row) for row in file2}
    file2_dict = {get_key(row): row for row in file2}

    print(f"Завантажено рядків у file1: {len(file1)}, у file2: {len(file2)}\n")

    # 1. JOIN
    join_result = []
    for row1 in file1:
        key = get_key(row1)
        if key in file2_dict:
            join_result.append({
                'zip_code': key[0],
                'latitude': key[1],
                'longitude': key[2],
                'name_file1': row1.get('name', ''),
                'name_file2': file2_dict[key].get('name', '')
            })

    print(f"=== 1. JOIN РЕЗУЛЬТАТ ===")
    print(f"Знайдено спільних записів: {len(join_result)}")
    for item in join_result[:3]:
        print(item)
    print("-" * 40)

    # 2. UNION
    set1 = {get_key(row) for row in file1}
    union_keys = set1.union(set2)

    print(f"=== 2. UNION РЕЗУЛЬТАТ ===")
    print(f"Загальна кількість унікальних комбінацій: {len(union_keys)}")
    print("-" * 40)

    # 3. NOT IN
    not_in_result = [row for row in file1 if get_key(row) not in set2]

    print(f"=== 3. NOT IN РЕЗУЛЬТАТ ===")
    print(f"Кількість записів з file1, яких немає в file2: {len(not_in_result)}")
    print("-" * 40)

    # 4. GROUP BY
    grouped_data = {}
    for row in file1:
        zip_code = row.get('zipcode', 'Unknown')
        zip_code = str(zip_code).strip() if zip_code is not None else 'No_Zip'

        lat = row.get('latitude')
        lon = row.get('longitude')
        lat_str = str(lat).strip() if lat is not None else ''
        lon_str = str(lon).strip() if lon is not None else ''

        if not zip_code:
            zip_code = "No_Zip"

        if zip_code not in grouped_data:
            grouped_data[zip_code] = []

        coord_pair = (lat_str, lon_str)
        if coord_pair not in grouped_data[zip_code]:
            grouped_data[zip_code].append(coord_pair)

    print(f"=== 4. GROUP BY РЕЗУЛЬТАТ ===")
    print(f"Всього унікальних поштових індексів: {len(grouped_data)}")
    count = 0
    for zip_code, coords in grouped_data.items():
        if count < 5:
            print(f"Zip Code: {zip_code} -> Кількість унікальних координат: {len(coords)}")
            count += 1

if __name__ == '__main__':
    main()
