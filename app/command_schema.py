def create_command(
    target_column,
    target_value,
    field,
    operation,
    new_value
):
    return {
        "target_column": target_column,
        "target_value": target_value,
        "field": field,
        "operation": operation,
        "new_value": new_value
    }