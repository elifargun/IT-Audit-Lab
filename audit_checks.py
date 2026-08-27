"""
IT Audit Lab - Automated User Access Review
=============================================

Performs simple ITGC-style checks against a user access CSV file:

  1. Former Employee Access Check
     Flags accounts still Active for users whose employment status is
     "Former Employee".

  2. Excessive Privilege Check
     Flags Specialist-level users who hold "CRM Admin" access.

  3. Segregation of Duties (SoD) Check
     Flags users who hold two access rights that should never be combined
     (e.g. can both create AND approve the same type of transaction).

Expected CSV columns:
    name, role, access, status, employment_status

The `access` column may contain multiple rights separated by ";"
(e.g. "Invoice Creation;Invoice Approval") so the SoD check can evaluate
combinations. A single-value access field (e.g. "CRM Admin") still works
fine for the other two checks.

Usage:
    python audit_checks.py --input users.csv
    python audit_checks.py --input users.csv --output findings.csv
"""

import argparse
import csv
import sys

# Pairs of access rights that violate Segregation of Duties when held together.
SOD_CONFLICTS = [
    ("Invoice Creation", "Invoice Approval"),
    ("Vendor Creation", "Payment Processing"),
    ("Payroll Entry", "Payroll Approval"),
]


def load_users(path):
    """Read the user access CSV into a list of dicts. Exits with a clear
    error message if the file is missing or unreadable."""
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        sys.exit(f"Error: input file not found: {path}")
    except OSError as e:
        sys.exit(f"Error reading {path}: {e}")


def get_field(user, field, default=""):
    """Safely read a field from a user row, tolerating missing columns
    or empty values instead of raising a KeyError."""
    value = user.get(field)
    return value.strip() if value else default


def check_former_employee_active(user):
    if get_field(user, "employment_status") == "Former Employee" and get_field(user, "status") == "Active":
        return {
            "user": get_field(user, "name"),
            "finding": "Active account for former employee",
            "risk_level": "CRITICAL",
            "detail": f"Access: {get_field(user, 'access')}, Status: {get_field(user, 'status')}",
        }
    return None


def check_excessive_privilege(user):
    if get_field(user, "role") == "Specialist" and get_field(user, "access") == "CRM Admin":
        return {
            "user": get_field(user, "name"),
            "finding": "Potential excessive privilege",
            "risk_level": "HIGH",
            "detail": f"Role: {get_field(user, 'role')}, Access: {get_field(user, 'access')}",
        }
    return None


def check_segregation_of_duties(user):
    access_list = [a.strip() for a in get_field(user, "access").split(";") if a.strip()]
    for duty_a, duty_b in SOD_CONFLICTS:
        if duty_a in access_list and duty_b in access_list:
            return {
                "user": get_field(user, "name"),
                "finding": f"SoD conflict: '{duty_a}' + '{duty_b}'",
                "risk_level": "HIGH",
                "detail": f"Access: {', '.join(access_list)}",
            }
    return None


CHECKS = [check_former_employee_active, check_excessive_privilege, check_segregation_of_duties]


def run_checks(users):
    """Run every check against every user and collect all findings."""
    findings = []
    for user in users:
        for check in CHECKS:
            result = check(user)
            if result:
                findings.append(result)
    return findings


def print_findings(findings):
    if not findings:
        print("No findings. All checks passed.")
        return
    for f in findings:
        print("\nACCESS CONTROL FINDING")
        print("-" * 30)
        print(f"User: {f['user']}")
        print(f"Finding: {f['finding']}")
        print(f"Detail: {f['detail']}")
        print(f"Risk Level: {f['risk_level']}")


def write_findings_csv(findings, path):
    fieldnames = ["user", "finding", "risk_level", "detail"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)


def main():
    parser = argparse.ArgumentParser(description="IT Audit Lab - automated user access review")
    parser.add_argument("--input", default="users.csv", help="Path to the user access CSV file")
    parser.add_argument("--output", default=None, help="Optional path to write findings as a CSV report")
    args = parser.parse_args()

    users = load_users(args.input)
    findings = run_checks(users)
    print_findings(findings)

    if args.output:
        write_findings_csv(findings, args.output)
        print(f"\n{len(findings)} finding(s) written to {args.output}")


if __name__ == "__main__":
    main()
