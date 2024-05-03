def result_to_dict(result):
    print(result[0])
    """
    Convert query result to a list of dictionaries.

    Args:
        result: Result of the database query (list of tuples).

    Returns:
        List of dictionaries where each dictionary represents a row of the query result.
    """
    dicts = []
    for row in result:
        row_dict = {}
        for column, value in zip(result.keys(), row):
            row_dict[column] = value
        dicts.append(row_dict)
    return dicts