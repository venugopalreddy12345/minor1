import re


def parse_salary_value(value):
    value = value.strip().lower().replace(",", "")

    if value.endswith("k"):
        number = float(value[:-1])
        return int(number * 1000)

    return int(value)


def parse_command(command):
    # Numeric salary update
    salary_pattern = r"update\s+(.+?)\s+salary\s+to\s+([\d,]+(?:\.\d+)?k?)"

    match = re.search(salary_pattern, command, re.IGNORECASE)

    if match:
        candidate = match.group(1).strip()
        salary = parse_salary_value(match.group(2))

        return {
            "target_column": "Candidate",
            "target_value": candidate,
            "field": "Salary",
            "operation": "update",
            "new_value": salary
        }

    # Text address update
    address_pattern = r"change\s+(.+?)\s+address\s+to\s+(.+)"

    match = re.search(address_pattern, command, re.IGNORECASE)

    if match:
        candidate = match.group(1).strip()
        address = match.group(2).strip()

        return {
            "target_column": "Candidate",
            "target_value": candidate,
            "field": "Address",
            "operation": "update",
            "new_value": address
        }

    raise ValueError("Could not understand the command.")