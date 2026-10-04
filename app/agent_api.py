from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.file_manager import (
    select_excel_file,
    get_file_path
)

from app.file_access import check_file_access

from app.excel_reader import (
    read_excel_structure,
    find_excel_values
)

from app.prompt_analyzer import analyze_prompt
from app.command_validator import validate_command
from app.decision_engine import choose_execution_method
from app.target_finder import find_target
from app.execution_engine import execute_command

from app.verifier import (
    verify_cell,
    verify_row,
    verify_row_deleted
)

from app.result import create_result


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExcelCommand(BaseModel):

    file_id: str
    prompt: str


@app.get("/")
def root():

    return {
        "message": "AI Excel Automation Agent",
        "status": "running"
    }


@app.post("/select-file")
def select_file():

    try:

        return select_excel_file()

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.post("/execute")
def execute_excel_command(
    command_request: ExcelCommand
):

    try:

        # ==================================================
        # 1. GET FILE
        # ==================================================

        file_path = get_file_path(
            command_request.file_id
        )

        prompt = command_request.prompt

        # ==================================================
        # 2. CHECK ACCESS
        # ==================================================

        check_file_access(file_path)

        # ==================================================
        # 3. READ STRUCTURE
        # ==================================================

        excel_structure = read_excel_structure(
            file_path
        )

        # ==================================================
        # 4. AI UNDERSTANDS REQUEST
        # ==================================================

        command = analyze_prompt(
            prompt=prompt,
            excel_structure=excel_structure
        )

        # ==================================================
        # 5. VALIDATE COMMAND
        # ==================================================

        validate_command(
            command=command,
            excel_structure=excel_structure
        )

        operation = command["operation"]

        # ==================================================
        # 6. READ OPERATIONS
        # ==================================================

        if operation in {
            "read",
            "find"
        }:

            read_result = find_excel_values(
                file_path=file_path,
                target_column=command.get(
                    "target_column"
                ),
                target_value=command.get(
                    "target_value"
                ),
                field=command.get(
                    "field"
                )
            )

            return {
                "status": "COMPLETED",
                "file": file_path,
                "sheet": excel_structure["sheet"],
                "prompt": prompt,
                "operation": operation,
                "result": read_result,
                "verification": "PASSED",
                "file_id": command_request.file_id
            }

        # ==================================================
        # 7. CHOOSE EXECUTION METHOD
        # ==================================================

        execution_method = choose_execution_method(
            command
        )

        # ==================================================
        # 8. ADD ROW
        # ==================================================

        if operation == "add_row":

            updated = execute_command(
                file_path=file_path,
                target=None,
                command=command,
                execution_method=execution_method
            )

            verification = verify_row(
                file_path=file_path,
                row=updated["row"],
                expected_values=updated["values"]
            )

            return {
                "status": (
                    "COMPLETED"
                    if verification["passed"]
                    else "FAILED"
                ),
                "file": file_path,
                "sheet": excel_structure["sheet"],
                "row": updated["row"],
                "values": updated["values"],
                "verification": (
                    "PASSED"
                    if verification["passed"]
                    else "FAILED"
                ),
                "verification_details": verification,
                "prompt": prompt,
                "operation": operation,
                "execution_method": execution_method,
                "file_id": command_request.file_id
            }

        # ==================================================
        # 9. FIND TARGET
        # ==================================================

        target = find_target(
            file_path=file_path,
            target_column=command["target_column"],
            target_value=command["target_value"],
            target_field=command.get("field")
            or command["target_column"]
        )

        # ==================================================
        # 10. EXECUTE
        # ==================================================

        updated = execute_command(
            file_path=file_path,
            target=target,
            command=command,
            execution_method=execution_method
        )

        # ==================================================
        # 11. VERIFY DELETE
        # ==================================================

        if operation == "delete_row":

            verification = verify_row_deleted(
                file_path=file_path,
                target_column=command["target_column"],
                target_value=command["target_value"]
            )

            return create_result(
                file_path=file_path,
                sheet_name=excel_structure["sheet"],
                operation=operation,
                verification_passed=verification["passed"],
                row=updated["row"],
                deleted_values=updated["deleted_values"],
                verification_details=verification,
                prompt=prompt,
                execution_method=execution_method,
                file_id=command_request.file_id
            )

        # ==================================================
        # 12. VERIFY NORMAL CELL MODIFICATION
        # ==================================================

        verification = verify_cell(
            file_path=file_path,
            cell=updated["cell"],
            expected_value=updated["new_value"]
        )

        # ==================================================
        # 13. GENERIC RESULT
        # ==================================================

        return create_result(
            file_path=file_path,
            sheet_name=excel_structure["sheet"],
            operation=operation,
            verification_passed=verification["passed"],
            cell=updated["cell"],
            row=target["row"],
            column=target["column"],
            old_value=updated["old_value"],
            new_value=updated["new_value"],
            verification_details=verification,
            prompt=prompt,
            execution_method=execution_method,
            command=command,
            file_id=command_request.file_id
        )

    except Exception as error:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )