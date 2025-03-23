async def compare_matching_keys(first_dict, second_dict):
    """Сравнивает значения совпадающих ключей между двумя словарям и возвращает True, если совпадают."""

    for key in first_dict:
        if key in second_dict and first_dict[key] != second_dict[key]:
            return False

    return True
