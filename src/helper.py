from datetime import datetime


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

def calculate_age(do):
    """
    Calculate age based on the date of birth.
    
    Args:
    dob (datetime.date): The date of birth as a datetime.date object.

    Returns:
    int: Age in years.
    """
    dob = datetime.strptime(do, "%Y-%m-%d").date()
    # Get the current date
    today = datetime.now().date()

    # Calculate preliminary age
    age = today.year - dob.year

    # Adjust based on whether the birthday has already occurred this year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age