"""Beginner-friendly, read-only validator for the Lab 01 mock IAM CSV files.

This script reports possible data-quality and governance issues. It does not
change any identity or access. Findings must be investigated before remediation.
"""

import csv
from datetime import date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def read_csv(filename):
    """Read a CSV file into a list of dictionaries."""
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def parse_date(value):
    """Convert YYYY-MM-DD to a date; return None for a blank date."""
    value = (value or "").strip()
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def main():
    today = date.today()
    identities = read_csv("identities.csv")
    roles = read_csv("roles.csv")
    assignments = read_csv("role_assignments.csv")

    findings = []

    # Index identities and roles so an assignment can be checked quickly.
    identity_by_id = {}
    duplicate_identity_ids = set()
    for identity in identities:
        identity_id = (identity.get("identity_id") or "").strip()
        if not identity_id:
            findings.append(("HIGH", "Identity record has a blank identity_id."))
        elif identity_id in identity_by_id:
            duplicate_identity_ids.add(identity_id)
        else:
            identity_by_id[identity_id] = identity

    for identity_id in sorted(duplicate_identity_ids):
        findings.append(("HIGH", f"Duplicate identity_id: {identity_id}"))

    role_by_id = {}
    for role in roles:
        role_id = (role.get("role_id") or "").strip()
        if role_id and role_id in role_by_id:
            findings.append(("HIGH", f"Duplicate role_id: {role_id}"))
        elif role_id:
            role_by_id[role_id] = role

    # Check that the data has required headers before doing comparisons.
    required_identity_fields = {
        "identity_id", "display_name", "department", "status", "end_date"
    }
    required_role_fields = {"role_id", "role_name", "department", "entitlement"}
    required_assignment_fields = {"assignment_id", "identity_id", "role_id"}

    if identities and not required_identity_fields.issubset(identities[0].keys()):
        missing = sorted(required_identity_fields - identities[0].keys())
        findings.append(("HIGH", f"identities.csv missing columns: {', '.join(missing)}"))
    if roles and not required_role_fields.issubset(roles[0].keys()):
        missing = sorted(required_role_fields - roles[0].keys())
        findings.append(("HIGH", f"roles.csv missing columns: {', '.join(missing)}"))
    if assignments and not required_assignment_fields.issubset(assignments[0].keys()):
        missing = sorted(required_assignment_fields - assignments[0].keys())
        findings.append(("HIGH", f"role_assignments.csv missing columns: {', '.join(missing)}"))

    # Flag lifecycle data that merits review.
    for identity in identities:
        identity_id = (identity.get("identity_id") or "UNKNOWN").strip()
        status = (identity.get("status") or "").strip().lower()
        end_date_text = (identity.get("end_date") or "").strip()
        if end_date_text:
            try:
                end_date = parse_date(end_date_text)
                if status == "active" and end_date and end_date < today:
                    findings.append((
                        "HIGH",
                        f"Active identity {identity_id} has a past end_date ({end_date.isoformat()})."
                    ))
            except ValueError:
                findings.append(("HIGH", f"Identity {identity_id} has invalid end_date: {end_date_text}"))

    seen_pairs = set()
    seen_assignment_ids = set()
    for assignment in assignments:
        assignment_id = (assignment.get("assignment_id") or "").strip()
        identity_id = (assignment.get("identity_id") or "").strip()
        role_id = (assignment.get("role_id") or "").strip()
        pair = (identity_id, role_id)

        if assignment_id and assignment_id in seen_assignment_ids:
            findings.append(("HIGH", f"Duplicate assignment_id: {assignment_id}"))
        seen_assignment_ids.add(assignment_id)

        if pair in seen_pairs:
            findings.append(("MEDIUM", f"Duplicate role assignment: {identity_id} / {role_id}"))
        seen_pairs.add(pair)

        identity = identity_by_id.get(identity_id)
        role = role_by_id.get(role_id)

        if not identity:
            findings.append(("HIGH", f"Assignment {assignment_id} references unknown identity: {identity_id}"))
            continue
        if not role:
            findings.append(("HIGH", f"Assignment {assignment_id} references unknown role: {role_id}"))
            continue

        status = (identity.get("status") or "").strip().lower()
        if status in {"terminated", "disabled", "inactive"}:
            findings.append((
                "HIGH",
                f"Inactive identity {identity_id} ({status}) still has role assignment {role_id}."
            ))

        identity_department = (identity.get("department") or "").strip().lower()
        role_department = (role.get("department") or "").strip().lower()
        if identity_department != role_department:
            findings.append((
                "MEDIUM",
                f"Department mismatch: {identity_id} is in {identity.get('department')} "
                f"but is assigned {role_id} for {role.get('department')}. Review business need."
            ))

    print("IAM Engineering Academy — Lab 01 data validation")
    print(f"Run date: {today.isoformat()}")
    print(f"Identities: {len(identities)} | Roles: {len(roles)} | Assignments: {len(assignments)}")
    print("-" * 72)

    if findings:
        for severity, message in findings:
            print(f"[{severity}] {message}")
        print("-" * 72)
        print(f"Validation completed: {len(findings)} finding(s). Investigate before remediation.")
        raise SystemExit(1)

    print("PASS: No validation issues found in the mock data.")
    print("Reminder: a clean file does not prove that access is appropriate; approvals and business need still matter.")


if __name__ == "__main__":
    main()
