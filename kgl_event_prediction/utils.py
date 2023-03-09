import re


def count_numerals(text: str):
    """
    :param text: any string that is suspected to contain numbers
    :return: the number of characters that are numeric
    """
    if text is None:
        return 0
    count = 0
    for c in text:
        if c.isnumeric():
            count += 1

    return count


def replace_var_in_sql(sql: str, var: str, text: str):
    """
    :param sql: sql-query string that should be modified
    :param var: name of the variable that should be replaced will be surrounded by $ escape characters in SQL
    :param text: string the variable should be replaced with
    :return: modified query
    """
    temp_var = "$"+str(var)+"$"
    return sql.replace(temp_var, str(text))


def remove_duplicates(element_list: list):
    """
    :param element_list: a list
    compares two adjecent elements and removes the second if identical to first.
    Removes all dublicates if list is ordered
    """
    prev = 0
    removal_list = []
    for i in range(1, len(element_list)):
        if element_list[prev] == element_list[i]:
            removal_list.append(element_list[i])
        prev = i

    for i in removal_list:
        element_list.remove(i)

    return element_list


def number_increase_in_string(string):
    def number_increase(match):
        num = int(match.group())
        return str(num + 1)

    pattern = r'\d+'
    return re.sub(pattern, number_increase, string)
