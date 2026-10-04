import xlwings as xw


def execute_option_b(file_path, target, command):
    """
    Execute an Excel modification through Microsoft Excel.
    """

    app = None
    workbook = None

    try:
        app = xw.App(visible=False)

        workbook = app.books.open(file_path)

        sheet = workbook.sheets.active

        cell = target["cell"]

        old_value = sheet.range(cell).value

        operation = command["operation"]

        # UPDATE
        if operation == "update":

            new_value = command["new_value"]

        # INCREASE
        elif operation == "increase":

            amount = command["amount"]
            unit = command["unit"]

            if unit == "percent":
                new_value = old_value + (
                    old_value * amount / 100
                )

            elif unit == "fixed":
                new_value = old_value + amount

            else:
                raise ValueError(
                    f"Unsupported unit: {unit}"
                )

        # DECREASE
        elif operation == "decrease":

            amount = command["amount"]
            unit = command["unit"]

            if unit == "percent":
                new_value = old_value - (
                    old_value * amount / 100
                )

            elif unit == "fixed":
                new_value = old_value - amount

            else:
                raise ValueError(
                    f"Unsupported unit: {unit}"
                )

        else:
            raise ValueError(
                f"Operation '{operation}' "
                "is not supported by Option B."
            )

        sheet.range(cell).value = new_value

        actual_new_value = sheet.range(cell).value

        workbook.save()

        return {
            "cell": cell,
            "old_value": old_value,
            "new_value": actual_new_value
        }

    finally:
        if workbook is not None:
            workbook.close()

        if app is not None:
            app.quit()