import pandas as pd

df1 = pd.read_csv('Barcelona1.csv')
df2 = pd.read_csv('Barcelona2.csv')

def get_key(row):
    return (
        row['name'],
        row['latitude'],
        row['longitude']
    )

def my_join(data1, data2):
    result = []
    records1 = data1.to_dict('records')
    records2 = data2.to_dict('records')
    data2_dict = {get_key(row2): row2 for row2 in records2}

    for row1 in records1:
        key = get_key(row1)
        if key in data2_dict:
            row2 = data2_dict[key]
            joined_row = {}

            for column, value in row1.items():
                joined_row['file1_' + column] = value
            for column, value in row2.items():
                joined_row['file2_' + column] = value
            result.append(joined_row)
    return result

def my_union(data1, data2):
    result = []
    seen = set()

    records1 = data1.to_dict('records')
    records2 = data2.to_dict('records')

    for records in (records1, records2):
        for row in records:
            key = get_key(row)

            # Пошук у set відбувається за O(1)
            if key not in seen:
                result.append(row)
                seen.add(key)
    return result

def my_not_in(data1, data2):
    result = []
    records1 = data1.to_dict('records')
    records2 = data2.to_dict('records')
    keys2 = {get_key(row) for row in records2}
    for row in records1:
        if get_key(row) not in keys2:
            result.append(row)
    return result

def my_group_by(data):
    groups = {}
    records = data.to_dict('records')
    for row in records:
        zipcode = row['zipcode']
        coordinates = (row['latitude'], row['longitude'])
        if zipcode not in groups:
            groups[zipcode] = set()
        groups[zipcode].add(coordinates)
    return groups

join_result = my_join(df1, df2)
union_result = my_union(df1, df2)
not_in_result = my_not_in(df1, df2)
group_result = my_group_by(df1)

print('JOIN')
print('Кількість записів ', len(join_result))
for row in join_result:
    print(row)

print('\nUNION')
print('Кількість записів ', len(union_result))
for row in union_result:
    print(row)

print('\nNOT-IN')
print('Кількість записів ', len(not_in_result))
for row in not_in_result:
    print(row)

print('\nGROUPBY')
for zipcode, coordinates in group_result.items():
    print(f'Zipcode: {zipcode}')
    for latitude, longitude in coordinates:
        print(f'  Latitude: {latitude}, Longitude: {longitude}')