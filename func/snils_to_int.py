def snils_to_int(STRING: str) -> int:
    if STRING is None:
        return 0

    try:
        int("".join(_ for _ in STRING if _ in "1234567890"))
    except ValueError:
        return 0
    else:
        return int("".join(_ for _ in STRING if _ in "1234567890"))
