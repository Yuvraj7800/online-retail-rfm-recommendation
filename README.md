# Task 1: Data Cleaning and Preprocessing

**Dataset:** Customer Personality Analysis / Marketing Campaign Data (Kaggle)
**File:** `marketing_campaign.csv` (tab-separated, 2240 rows x 29 columns)
**Tools used:** Python (Pandas, openpyxl)

## Objective
Clean and prepare the raw marketing campaign dataset by handling missing values, duplicates, inconsistent formats, and incorrect data types, following the task's mini-guide.

## Steps Performed

1. **Loaded raw data** — 2240 rows, 29 columns, tab-delimited.
2. **Renamed column headers** — converted all headers to lowercase with underscores (e.g. `Year_Birth` → `year_birth`) for clean, uniform naming.
3. **Identified missing values** — used `.isnull()`; found 24 missing values, all in `Income`.
4. **Handled missing values** — filled missing `income` values with the column **median** (51,381.50) using `.fillna()`. Median was used instead of mean because the column contains an extreme outlier.
5. **Checked for duplicates** — used `.duplicated()` on full rows and on `id`; found **0 duplicates** (verified, none removed).
6. **Standardized text values**:
   - `education`: trimmed whitespace, applied title case, fixed `"2n Cycle"` → `"2nd Cycle"`.
   - `marital_status`: trimmed whitespace, applied title case, relabeled non-standard placeholder values (`Absurd`, `YOLO`, `Alone` — 7 rows total) to `"Other"`.
7. **Converted date format** — parsed `dt_customer` from raw `dd-mm-yyyy` strings into proper datetime objects, then standardized the output back to a consistent `dd-mm-yyyy` text format.
8. **Fixed data types** — verified and cast all count/flag columns to `int64` and `income` to `float64`.
9. **Outlier treatment**:
   - Removed 3 rows with implausible `year_birth` values (1893, 1899, 1900 → implied ages of 114–121), clear data-entry errors.
   - Removed 1 row with an extreme `income` value (666,666 — roughly 4x the next highest value).
10. **Removed non-informative columns** — `z_costcontact` and `z_revenue` were constant across every row and dropped.
11. **Added derived columns** — `age` (2014 − year_birth), `total_spending` (sum of all `Mnt*` columns), `total_children` (kidhome + teenhome).
12. **Final quality check** — confirmed 0 missing values, 0 duplicate rows, and consistent data types across the cleaned dataset.

## Result

| | Raw | Cleaned |
|---|---|---|
| Rows | 2240 | 2236 |
| Columns | 29 | 30 |
| Missing values | 24 | 0 |
| Duplicate rows | 0 | 0 |

## Files in this submission
- `marketing_campaign.csv` — original raw dataset
- `marketing_campaign_cleaned.csv` — final cleaned dataset
- `Marketing_Campaign_Cleaned.xlsx` — cleaned dataset + formatted cleaning-summary sheet
- `clean_data.py` — Python (Pandas) script used to perform the cleaning
- `cleaning_log.txt` — console log of the cleaning run
- `README.md` — this file
