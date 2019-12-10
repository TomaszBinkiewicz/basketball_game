def validate_int(x):
    try:
        x = int(x)
    except (ValueError, TypeError):
        return False
    else:
        return True


def validate_positive(x):
    return x >= 0


def validate_positive_int(x):
    if validate_int(x):
        return validate_positive(int(x))
    return False
