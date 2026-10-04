def validate_command(command, excel_structure):

    if not isinstance(command, dict):
        raise ValueError(
            "AI command must be a JSON object."
        )

    if "operation" not in command:
        raise ValueError(
            "AI command is missing required field: operation"
        )

    operation = command["operation"]

    if not isinstance(operation, str):
        raise ValueError(
            "AI command operation must be a string."
        )

    operation = operation.strip().lower()

    if not operation:
        raise ValueError(
            "AI command operation cannot be empty."
        )

    excel_columns = excel_structure.get(
        "columns",
        []
    )

    def validate_column(
        column_name,
        field_name
    ):

        if column_name is None:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        if column_name not in excel_columns:
            raise ValueError(
                f"{field_name} '{column_name}' "
                "does not exist in Excel."
            )

    def validate_target():

        if "target_column" not in command:
            raise ValueError(
                "AI command is missing required field: "
                "target_column"
            )

        if "target_value" not in command:
            raise ValueError(
                "AI command is missing required field: "
                "target_value"
            )

        validate_column(
            command["target_column"],
            "Target column"
        )

        if command["target_value"] is None:
            raise ValueError(
                "Target value cannot be empty."
            )

    # ==================================================
    # READ
    # ==================================================

    if operation == "read":

        if "target_column" in command:

            validate_column(
                command["target_column"],
                "Target column"
            )

        if "target_value" in command:

            if command["target_value"] is None:
                raise ValueError(
                    "Target value cannot be empty."
                )

        if "field" in command:

            validate_column(
                command["field"],
                "Field"
            )

        return True

    # ==================================================
    # FIND
    # ==================================================

    if operation == "find":

        validate_target()

        if "field" not in command:
            raise ValueError(
                "Find operation requires field."
            )

        validate_column(
            command["field"],
            "Field"
        )

        return True

    # ==================================================
    # ADD ROW
    # ==================================================

    if operation == "add_row":

        if "values" not in command:
            raise ValueError(
                "AI command is missing required field: values"
            )

        values = command["values"]

        if not isinstance(values, dict):
            raise ValueError(
                "The 'values' field must be an object."
            )

        if not values:
            raise ValueError(
                "At least one value is required "
                "to add a new row."
            )

        for column_name in values:

            validate_column(
                column_name,
                "Column"
            )

        return True

    # ==================================================
    # DELETE ROW
    # ==================================================

    if operation == "delete_row":

        validate_target()

        if "field" in command:
            raise ValueError(
                "Delete operation must identify a row, "
                "not a field."
            )

        return True

    # ==================================================
    # OTHER TARGETED OPERATIONS
    # ==================================================

    validate_target()

    if "field" not in command:
        raise ValueError(
            "AI command is missing required field: field"
        )

    validate_column(
        command["field"],
        "Field"
    )

    if operation == "update":

        if "new_value" not in command:
            raise ValueError(
                "AI command is missing required field: "
                "new_value"
            )

        if command["new_value"] is None:
            raise ValueError(
                "New value cannot be empty."
            )

    elif operation in {
        "increase",
        "decrease"
    }:

        if "amount" not in command:
            raise ValueError(
                "AI command is missing required field: amount"
            )

        if "unit" not in command:
            raise ValueError(
                "AI command is missing required field: unit"
            )

        if command["amount"] is None:
            raise ValueError(
                "Amount cannot be empty."
            )

        if command["unit"] not in {
            "percent",
            "fixed"
        }:
            raise ValueError(
                "Unit must be either "
                "'percent' or 'fixed'."
            )

    else:

        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return True