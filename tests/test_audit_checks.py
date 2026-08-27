"""
Unit tests for audit_checks.py

Run with:
    pytest tests/
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from audit_checks import (
    check_excessive_privilege,
    check_former_employee_active,
    check_segregation_of_duties,
    get_field,
    load_users,
    run_checks,
)


# ---------------------------------------------------------------------------
# check_former_employee_active
# ---------------------------------------------------------------------------

def test_former_employee_with_active_account_is_flagged():
    user = {"name": "Test User", "employment_status": "Former Employee", "status": "Active", "access": "CRM"}
    result = check_former_employee_active(user)
    assert result is not None
    assert result["risk_level"] == "CRITICAL"


def test_former_employee_with_inactive_account_is_not_flagged():
    user = {"name": "Test User", "employment_status": "Former Employee", "status": "Inactive", "access": "CRM"}
    assert check_former_employee_active(user) is None


def test_current_employee_with_active_account_is_not_flagged():
    user = {"name": "Test User", "employment_status": "Current Employee", "status": "Active", "access": "CRM"}
    assert check_former_employee_active(user) is None


# ---------------------------------------------------------------------------
# check_excessive_privilege
# ---------------------------------------------------------------------------

def test_specialist_with_crm_admin_is_flagged():
    user = {"name": "Test User", "role": "Specialist", "access": "CRM Admin"}
    result = check_excessive_privilege(user)
    assert result is not None
    assert result["risk_level"] == "HIGH"


def test_manager_with_crm_admin_is_not_flagged():
    user = {"name": "Test User", "role": "Manager", "access": "CRM Admin"}
    assert check_excessive_privilege(user) is None


# ---------------------------------------------------------------------------
# check_segregation_of_duties
# ---------------------------------------------------------------------------

def test_conflicting_access_is_flagged():
    user = {"name": "Test User", "access": "Vendor Creation;Payment Processing"}
    result = check_segregation_of_duties(user)
    assert result is not None
    assert result["risk_level"] == "HIGH"


def test_single_access_right_is_not_flagged():
    user = {"name": "Test User", "access": "Vendor Creation"}
    assert check_segregation_of_duties(user) is None


def test_non_conflicting_combo_is_not_flagged():
    user = {"name": "Test User", "access": "Vendor Creation;Reporting"}
    assert check_segregation_of_duties(user) is None


# ---------------------------------------------------------------------------
# edge cases / robustness
# ---------------------------------------------------------------------------

def test_missing_fields_do_not_raise():
    user = {"name": "Incomplete User"}
    assert check_former_employee_active(user) is None
    assert check_excessive_privilege(user) is None
    assert check_segregation_of_duties(user) is None


def test_get_field_returns_default_when_missing():
    assert get_field({}, "role") == ""
    assert get_field({}, "role", "N/A") == "N/A"


def test_load_users_missing_file_exits():
    import pytest as _pytest
    with _pytest.raises(SystemExit):
        load_users("this_file_does_not_exist.csv")


# ---------------------------------------------------------------------------
# integration: run_checks against a full sample CSV
# ---------------------------------------------------------------------------

def test_run_checks_against_sample_csv(tmp_path):
    csv_path = tmp_path / "users.csv"
    rows = [
        {"name": "A", "role": "Specialist", "access": "CRM Admin", "status": "Active", "employment_status": "Current Employee"},
        {"name": "B", "role": "Analyst", "access": "Reporting", "status": "Active", "employment_status": "Former Employee"},
        {"name": "C", "role": "Manager", "access": "Vendor Creation;Payment Processing", "status": "Active", "employment_status": "Current Employee"},
        {"name": "D", "role": "Clerk", "access": "Invoice Creation", "status": "Active", "employment_status": "Current Employee"},
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    users = load_users(str(csv_path))
    findings = run_checks(users)

    flagged_names = {f["user"] for f in findings}
    assert flagged_names == {"A", "B", "C"}
    assert len(findings) == 3
