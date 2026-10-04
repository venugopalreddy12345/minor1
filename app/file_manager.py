from pathlib import Path
import uuid
import tkinter as tk
from tkinter import filedialog


# Stores the relationship between a file_id and
# the actual Excel file on the user's computer.
_file_registry = {}


def register_file(file_path):
    """
    Register a local Excel file and generate a file_id.
    """

    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"Excel file not found: {path}"
        )

    if path.suffix.lower() != ".xlsx":
        raise ValueError(
            "Only .xlsx files are supported."
        )

    file_id = str(uuid.uuid4())

    _file_registry[file_id] = str(path)

    return {
        "file_id": file_id,
        "file_name": path.name
    }


def select_excel_file():
    """
    Open the Windows file picker and let the user
    select an Excel file from their computer.
    """

    root = tk.Tk()
    root.withdraw()

    root.attributes("-topmost", True)
    root.after(100, root.attributes, "-topmost", False)

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[
            ("Excel files", "*.xlsx"),
            ("Excel files", "*.xlsm"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    if not file_path:
        raise ValueError(
            "No Excel file was selected."
        )

    return register_file(file_path)


def get_file_path(file_id):
    """
    Resolve a file_id to the actual local file path.
    """

    if file_id not in _file_registry:
        raise ValueError(
            f"Unknown file_id: {file_id}"
        )

    file_path = _file_registry[file_id]

    if not Path(file_path).exists():
        raise FileNotFoundError(
            f"Registered Excel file no longer exists: {file_path}"
        )

    return file_path


def remove_file(file_id):
    """
    Remove a file from the current registry.
    """

    if file_id in _file_registry:
        del _file_registry[file_id]