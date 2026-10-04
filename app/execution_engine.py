from app.excel_modifier import (
    modify_cell,
    add_row,
    delete_row
)

from app.excel_automation import execute_option_b


def execute_option_a(file_path, target, command):

    return modify_cell(
        file_path=file_path,
        cell=target["cell"],
        command=command
    )


def execute_add_row(file_path, command):

    return add_row(
        file_path=file_path,
        values=command["values"]
    )


def execute_delete_row(file_path, target):

    return delete_row(
        file_path=file_path,
        row=target["row"]
    )


def execute_command(
    file_path,
    target,
    command,
    execution_method
):

    operation = command.get("operation")

    if operation == "add_row":

        return execute_add_row(
            file_path=file_path,
            command=command
        )

    if operation == "delete_row":

        if target is None:
            raise ValueError(
                "Delete operation requires a target row."
            )

        return execute_delete_row(
            file_path=file_path,
            target=target
        )

    if target is None:
        raise ValueError(
            "This operation requires a specific Excel target."
        )

    if execution_method == "OPTION_A":

        return execute_option_a(
            file_path=file_path,
            target=target,
            command=command
        )

    if execution_method == "OPTION_B":

        return execute_option_b(
            file_path=file_path,
            target=target,
            command=command
        )

    raise ValueError(
        f"Unknown execution method: {execution_method}"
    )