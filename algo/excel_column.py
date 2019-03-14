def get_column_id(column_name):
    if not column_name:
        raise ValueError('name cannot be empty')

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(letters)
    mapping = {l: i + 1 for i, l in enumerate(letters)}

    total = 0
    for digit in column_name.upper():
        num = mapping[digit]
        total = total * base + num

    return total

def get_column_name(column_id):
    if column_id <= 0:
        raise ValueError('id must great than 0')

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(letters)

    parts = []
    while column_id > 0:
        column_id, idx = divmod(column_id - 1, base)
        parts.append(letters[idx])

    return ''.join(reversed(parts))

def test(id_or_name):
    if isinstance(id_or_name, str):
        column_name = id_or_name.upper()
        column_id = get_column_id(column_name)
        print column_name, column_id, get_column_name(column_id)
    else:
        column_id = id_or_name
        column_name = get_column_name(column_id)
        print column_id, column_name, get_column_id(column_name)
