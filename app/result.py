def create_result(
    file_path,
    sheet_name,
    operation,
    verification_passed,
    **details
):
    """
    Create a generic result for any Excel operation.

    The result is not tied to a specific type of operation.
    Operation-specific information is stored inside details.
    """

    result = {
        "status": (
            "COMPLETED"
            if verification_passed
            else "FAILED"
        ),
        "file": file_path,
        "sheet": sheet_name,
        "operation": operation,
        "verification": (
            "PASSED"
            if verification_passed
            else "FAILED"
        )
    }

    result.update(details)

    return result


def print_result(result):

    print("\n" + "=" * 40)
    print("TASK RESULT")
    print("=" * 40)

    for key, value in result.items():

        label = key.replace(
            "_",
            " "
        ).title()

        print(
            f"{label}: {value}"
        )

    print("=" * 40)