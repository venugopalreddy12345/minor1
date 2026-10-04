import json

from app.llm_client import ask_llm


def analyze_prompt(prompt, excel_structure):

    columns = excel_structure["columns"]

    analysis_prompt = f"""
You are an Excel command parser.

Convert the user's request into EXACTLY ONE JSON object.

Excel columns:
{columns}

The normal row-identification column is:
"Candidate"

==================================================
GENERAL RULES
==================================================

1. Understand the user's intent.
2. Use ONLY columns that exist in the Excel columns list.
3. Never invent a column.
4. Read/find operations NEVER modify Excel.
5. Return ONLY valid JSON.
6. Return exactly ONE JSON object.
7. Do not return Markdown.
8. Do not explain anything.
9. Remove possessive "'s" from person names.
10. Preserve the actual person name exactly as identified
    from the user's request, except for removing "'s".
11. Natural-language wording can vary. Identify the
    underlying intent rather than requiring exact phrases.

==================================================
SUPPORTED OPERATIONS
==================================================

update
increase
decrease
find
read
add_row
delete_row

==================================================
UPDATE
==================================================

Use update when the user wants to replace an existing
value for one specific person.

Examples:

Update Venus salary to 150000

{{
  "operation": "update",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary",
  "new_value": 150000
}}

Change Venus's salary to 95000

{{
  "operation": "update",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary",
  "new_value": 95000
}}

Make Alex's address Bangalore

{{
  "operation": "update",
  "target_column": "Candidate",
  "target_value": "Alex",
  "field": "Address",
  "new_value": "Bangalore"
}}

==================================================
INCREASE
==================================================

Use increase when the user wants to increase an existing
numeric value.

Example:

Increase Venus salary by 10%

{{
  "operation": "increase",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary",
  "amount": 10,
  "unit": "percent"
}}

Example:

Increase Priya salary by 5000

{{
  "operation": "increase",
  "target_column": "Candidate",
  "target_value": "Priya",
  "field": "Salary",
  "amount": 5000,
  "unit": "fixed"
}}

Natural wording:

Give Alex a 25% salary hike

{{
  "operation": "increase",
  "target_column": "Candidate",
  "target_value": "Alex",
  "field": "Salary",
  "amount": 25,
  "unit": "percent"
}}

==================================================
DECREASE
==================================================

Use decrease when the user wants to decrease an existing
numeric value.

Example:

Decrease Venus salary by 10%

{{
  "operation": "decrease",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary",
  "amount": 10,
  "unit": "percent"
}}

Example:

Decrease Priya salary by 5000

{{
  "operation": "decrease",
  "target_column": "Candidate",
  "target_value": "Priya",
  "field": "Salary",
  "amount": 5000,
  "unit": "fixed"
}}

Natural wording:

Cut Alex's salary by 10000

{{
  "operation": "decrease",
  "target_column": "Candidate",
  "target_value": "Alex",
  "field": "Salary",
  "amount": 10000,
  "unit": "fixed"
}}

==================================================
FIND
==================================================

Use find when the user wants ONE SPECIFIC FIELD
from ONE SPECIFIC PERSON.

The user does NOT need to use the word "find".

Recognize natural-language questions that ask for the
current value of one particular field belonging to one
particular person.

These all mean FIND:

What is Priya's address?

What address does Priya have?

Tell me Priya's address.

Show Priya's address.

What is Priya's salary?

What salary is Priya receiving?

What salary is Venus currently receiving?

How much does Venus earn?

Tell me Venus's salary.

What is Alex's current salary?

Which address belongs to Alex?

For all such requests:

target_column = "Candidate"
target_value = the person's name
field = the requested Excel column

Example:

What is Priya's address?

{{
  "operation": "find",
  "target_column": "Candidate",
  "target_value": "Priya",
  "field": "Address"
}}

Example:

What salary is Venus currently receiving?

{{
  "operation": "find",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary"
}}

Example:

How much does Alex earn?

{{
  "operation": "find",
  "target_column": "Candidate",
  "target_value": "Alex",
  "field": "Salary"
}}

IMPORTANT:

Do NOT require the user to explicitly say "find".

Determine the requested field from the meaning of the
question.

For example:

"How much does Venus earn?"
means field = "Salary"

"What address does Alex have?"
means field = "Address"

==================================================
READ
==================================================

Use read when the user wants multiple fields/details,
an entire row, an entire column, or all rows.

--------------------------------------------------
ONE PERSON + ALL DETAILS
--------------------------------------------------

Example:

Show me everything about Rahul

{{
  "operation": "read",
  "target_column": "Candidate",
  "target_value": "Rahul"
}}

Example:

Tell me everything you know about Alex

{{
  "operation": "read",
  "target_column": "Candidate",
  "target_value": "Alex"
}}

Example:

Show me Alex's details

{{
  "operation": "read",
  "target_column": "Candidate",
  "target_value": "Alex"
}}

--------------------------------------------------
ONE COLUMN
--------------------------------------------------

Example:

Show all candidate names

{{
  "operation": "read",
  "field": "Candidate"
}}

Example:

Show me all salaries

{{
  "operation": "read",
  "field": "Salary"
}}

Example:

List all addresses

{{
  "operation": "read",
  "field": "Address"
}}

--------------------------------------------------
ALL ROWS
--------------------------------------------------

Use read with NO target_column, target_value, or field
when the user wants all employee records.

Examples:

Show me everyone

{{
  "operation": "read"
}}

Show me all employee records

{{
  "operation": "read"
}}

Show the entire spreadsheet

{{
  "operation": "read"
}}

IMPORTANT:

Do not convert "all employee records" into a
single-column read.

==================================================
ADD ROW
==================================================

Use add_row when the user wants a NEW person,
employee, record, or row.

Example:

Add Durden with salary 50000 and address London

{{
  "operation": "add_row",
  "values": {{
    "Candidate": "Durden",
    "Salary": 50000,
    "Address": "London"
  }}
}}

Example:

Add an employee named Mike with salary 55000

{{
  "operation": "add_row",
  "values": {{
    "Candidate": "Mike",
    "Salary": 55000,
    "Address": null
  }}
}}

Use actual Excel column names.

"50k" = 50000.
"1 lakh" = 100000.
"1L" = 100000.

Do not invent missing values.

If a column was not provided by the user,
use null for that column.

==================================================
DELETE ROW
==================================================

Use delete_row when the user wants to remove/delete
an EXISTING row.

Natural-language examples:

Delete Rahul's row
Remove Rahul
Delete the row containing Rahul
Remove Rahul from the sheet
Delete Rahul's record
Delete Rahul's details

All of these mean deleting the ENTIRE row.

Return:

{{
  "operation": "delete_row",
  "target_column": "Candidate",
  "target_value": "Rahul"
}}

IMPORTANT:

delete_row removes the ENTIRE row.

Do NOT include "field".

Do NOT invent a row number.

The row number will be found by the execution system.

If the user identifies a person using Candidate,
use:

target_column = "Candidate"

If the target person occurs more than once,
do NOT guess which row should be deleted.

The execution system will detect the ambiguity.

==================================================
IMPORTANT DISTINCTION
==================================================

One specific person + one specific field
= find

Example:

What is Venus's salary?

{{
  "operation": "find",
  "target_column": "Candidate",
  "target_value": "Venus",
  "field": "Salary"
}}

One specific person + all their details
= read

Example:

Show me Venus's details

{{
  "operation": "read",
  "target_column": "Candidate",
  "target_value": "Venus"
}}

One entire column
= read

Example:

Show me all salaries

{{
  "operation": "read",
  "field": "Salary"
}}

All employee records
= read

Example:

Show me all employee records

{{
  "operation": "read"
}}

==================================================
SAFETY
==================================================

- Never invent values.
- Never invent columns.
- Never invent row numbers.
- Delete only an explicitly identified existing row.
- If the request is ambiguous, do not guess.
- Return exactly one JSON object.
- Return ONLY JSON.

==================================================
USER REQUEST
==================================================

{prompt}
"""

    response = ask_llm(
        prompt=analysis_prompt,
        model="llama3.2:3b"
    )

    print("\n========== OLLAMA RESPONSE ==========")
    print(response)
    print("======================================")

    if response is None:
        raise ValueError(
            "Ollama returned None."
        )

    response = str(response).strip()

    if not response:
        raise ValueError(
            "Ollama returned an empty response."
        )

    if "```" in response:

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "Ollama did not return JSON.\n\n"
            f"Response:\n{response}"
        )

    json_text = response[start:end + 1]

    try:

        command = json.loads(json_text)

    except json.JSONDecodeError as error:

        raise ValueError(
            "Ollama returned invalid JSON.\n\n"
            f"Response:\n{response}\n\n"
            f"Error:\n{error}"
        )

    if not isinstance(command, dict):

        raise ValueError(
            "AI command must be a JSON object."
        )

    print("\n========== AI COMMAND ==========")
    print(command)
    print("================================")

    return command