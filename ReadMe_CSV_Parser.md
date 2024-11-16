# ReadMe for CSV Parser

## Overview
This script processes a CSV leaderboard file by updating it with new data from another CSV file. It adds new columns and rows, sorts the data, and ensures the leaderboard remains consistent. The processed data is saved back to the original leaderboard file.

---

## Features
1. **Processing New Data:**
   - Reads new data from an input file and updates existing records in the leaderboard.
   - Adds new rows if a match is not found in the leaderboard.

2. **Dynamic Column Handling:**
   - Finds the last `R` column dynamically and adds a new column for future data.

3. **Sorting:**
   - Sorts rows in descending order based on the `Total` column.
   - Updates row indices (`Column1`) accordingly.

4. **Validation and Adjustment:**
   - Ensures `Total` values do not exceed 150.
   - Adjusts related fields (`Spent`, `Column28`) based on `Total`.

5. **Output:**
   - Saves the updated leaderboard to the same CSV file, ensuring the updated order and data.

---

## How to Use

### Prerequisites
- Python 3.x
- `pandas` library installed. Install it via pip:
  ```bash
  pip install pandas
  ```

## IMPORTANT!!!
**FILL YOUR LEADERBOARD TABLE WITH COLUMN NAMES**
-Column1, Column2
-Percent (column after 'Spent')

**IN NEW DATA FILE NAME YOUR COLUMNS(name, score)**

### Script Execution
1. Replace `"leaderboard_file_path"` and `"new_data_file_path"` in the script with the paths to your leaderboard and new data CSV files.
2. Run the script:
   ```bash
   python main.py
   ```

---

## Key Functions

### 1. **`sorter(frame_list)`**
   - Sorts a list of dictionary rows by the `Total` field in descending order.
   - Updates the `Column1` field with new positions.

### 2. **`csv_parser(leaderboard_csv, new_data_csv)`**
   - Main function that:
     1. Reads and parses the leaderboard file.
     2. Detects separators between tables.
     3. Updates existing rows with scores from the new data file.
     4. Adds new rows if no match is found.
     5. Sorts and appends the updated data back to the leaderboard.
     6. Saves the processed data to the original leaderboard file.

---

## Input Requirements
- **Leaderboard CSV:**
  - Must contain columns such as `Column1`, `Column2`, `Total`, `Spent`, and multiple `R` columns.
- **New Data CSV:**
  - Must contain `name` and `score` fields.

---

## Output
- The script saves the processed leaderboard back to the input file (`leaderboard_csv`).
- The order of rows and columns will be updated to reflect the changes.

---

## Troubleshooting
1. **Error: `KeyError` or `ValueError`:**
   - Ensure both CSV files have the required column names.
2. **Incorrect Sorting:**
   - Verify that the `Total` column in the leaderboard CSV contains numeric values.

---

## Author
This script is designed to automate leaderboard updates and sorting for competitive scenarios. Please customize paths and column names as needed for your specific use case.
