def read_boolean_query_parameter(value):
    if value is not None:
        value = str(value).lower()
        if value in ('1', 'true'):
            return True
        if value in ('0', 'false'):
            return False
    return None
