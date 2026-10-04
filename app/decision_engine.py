def choose_execution_method(command):

    operation = command.get("operation")

    # ==================================================
    # OPERATIONS THAT USE OPENPYXL
    # ==================================================

    if operation in {
        "update",
        "increase",
        "decrease",
        "add_row",
        "delete_row"
    }:
        return "OPTION_A"

    # ==================================================
    # READ OPERATIONS
    # ==================================================

    if operation in {
        "read",
        "find"
    }:
        return "READ"

    raise ValueError(
        f"No execution method available for operation: "
        f"{operation}"
    )