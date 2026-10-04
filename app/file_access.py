from pathlib import Path
import openpyxl


def check_file_access(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Excel file not found: {path}"
        )

    if path.suffix.lower() != ".xlsx":
        raise ValueError(
            "Only .xlsx files are supported."
        )

    # Test whether the file can be opened for writing.
    try:
        with open(path, "r+b"):
            pass
    except PermissionError:
        raise PermissionError(
            "The Excel file is currently open or locked "
            "by another application. Please close it and try again."
        )

    return True


def open_excel_file(file_path):
    check_file_access(file_path)

    workbook = openpyxl.load_workbook(file_path)

    return workbook