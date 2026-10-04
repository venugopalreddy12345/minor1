"""
Generic operation schema.
"""


READ_OPERATIONS = {
    "read",
    "find"
}

ROW_OPERATIONS = {
    "add_row",
    "delete_row"
}

CELL_OPERATIONS = {
    "update",
    "increase",
    "decrease"
}


def is_read_operation(operation):
    return operation in READ_OPERATIONS


def is_row_operation(operation):
    return operation in ROW_OPERATIONS


def is_cell_operation(operation):
    return operation in CELL_OPERATIONS


def is_known_operation(operation):
    return (
        is_read_operation(operation)
        or is_row_operation(operation)
        or is_cell_operation(operation)
    )


def validate_operation_type(operation):

    if not isinstance(operation, str):
        raise ValueError(
            "Operation must be a string."
        )

    operation = operation.strip().lower()

    if not operation:
        raise ValueError(
            "Operation cannot be empty."
        )

    if not is_known_operation(operation):
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return True