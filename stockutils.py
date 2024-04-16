def get_column_name(data, param):
    columns = list(data.columns)
    index = -1
    for s in columns:
        if (s.__contains__(param)):
            print('column', s)
            index = columns.index(s)
            break
    return index