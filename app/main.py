from prompt_analyzer import analyze_prompt
from target_finder import find_target
from verifier import verify_cell
from result import create_result, print_result
from command_validator import validate_command
from file_access import check_file_access
from decision_engine import choose_execution_method
from execution_engine import execute_command
file_path = "employees.xlsx"
check_file_access(file_path)

# Read basic Excel structure
excel_structure = {
    "sheet": "Sheet1",
    "columns": [
        "Candidate",
        "Salary",
        "Address"
    ]
}

# User's natural-language command
prompt = "Decrease Venus salary by 10%"# Step 1: AI understands the command
command = analyze_prompt(
    prompt=prompt,
    excel_structure=excel_structure
)
# Validate AI command before touching Excel
validate_command(
    command=command,
    excel_structure=excel_structure
)
execution_method = choose_execution_method(command)

print("\nEXECUTION METHOD")
print("=" * 40)
print(execution_method)
print("=" * 40)

print("\nAI COMMAND")
print("=" * 40)
print(command)
print("=" * 40)


# Step 2: Find the exact Excel target
target = find_target(
    file_path=file_path,
    target_column=command["target_column"],
    target_value=command["target_value"],
    target_field=command["field"]
)


# Step 3: Modify Excel
updated = execute_command(
    file_path=file_path,
    target=target,
    command=command,
    execution_method=execution_method
)


# Step 4: Verify modification
verification = verify_cell(
    file_path=file_path,
    cell=updated["cell"],
    expected_value=updated["new_value"]
)


# Step 5: Create final result
final_result = create_result(
    file_path=file_path,
    sheet_name=excel_structure["sheet"],
    cell=updated["cell"],
    row=target["row"],
    column=target["column"],
    old_value=updated["old_value"],
    new_value=updated["new_value"],
    verification_passed=verification["passed"]
)


# Step 6: Display result
print_result(final_result)