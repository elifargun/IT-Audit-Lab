# IT Audit Lab

Hands-on IT audit and access control automation exercises using Python.

## Why I Built This

I wanted a small, working example of how ITGC-style access reviews can be
automated instead of done manually in a spreadsheet — the kind of check an
IT auditor or SOX/ITGC analyst runs when validating **user access controls**
and the **principle of least privilege**.

## Project Overview

This project performs an automated user access review using Python and CSV
data. The script reads user access records and flags potential access
control issues based on predefined audit rules — no manual cross-referencing
required.

## Audit Objective

The objective is to identify potential access control risks, including:

- Active accounts belonging to former employees
- Potential excessive privileges
- Segregation of Duties (SoD) conflicts
- Administrative access that may not be appropriate for the user's role

## Automated Controls

### 1. Former Employee Access Check
Flags users whose employment status is **Former Employee** while their
account status remains **Active**. This may indicate that access was not
revoked after termination. `Risk Level: CRITICAL`

### 2. Excessive Privilege Check
Flags Specialist-level users who hold **CRM Admin** access, reviewed against
the principle of least privilege. `Risk Level: HIGH`

### 3. Segregation of Duties (SoD) Check
Flags users who hold two access rights that should never be combined by the
same person — e.g. the ability to both **create** and **approve** the same
type of transaction. Conflicting pairs are defined in `SOD_CONFLICTS` inside
`audit_checks.py` and can be extended to match a real control matrix.
`Risk Level: HIGH`

## Usage

```bash
# Run against the default users.csv and print findings to the console
python audit_checks.py

# Run against a specific file and also save findings to a CSV report
python audit_checks.py --input users.csv --output findings.csv
```

### Sample output

```
ACCESS CONTROL FINDING
------------------------------
User: Elif Yıldız
Finding: SoD conflict: 'Vendor Creation' + 'Payment Processing'
Detail: Access: Vendor Creation, Payment Processing
Risk Level: HIGH

3 finding(s) written to findings.csv
```

## Running the Tests

Unit tests cover all three controls plus edge cases (missing fields, missing
input file).

```bash
pip install pytest
pytest tests/ -v
```

12 tests, all passing.

## Files

- `users.csv` — Sample user access dataset. The `access` column supports
  multiple rights separated by `;` (e.g. `Vendor Creation;Payment Processing`)
  so the SoD check can evaluate combinations.
- `audit_checks.py` — Python script that runs all three access review checks
  and optionally writes findings to a CSV report.
- `tests/test_audit_checks.py` — pytest unit and integration tests.

## Technologies

- Python (`csv`, `argparse`)
- pytest
- Git / GitHub

## Disclaimer

All users and data in this repository are fictional and created solely for
educational and portfolio purposes.
