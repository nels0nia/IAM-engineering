# IAM Engineering Academy — Lab 01: Identity Foundations

**Level:** Beginner  
**Theme:** Model identities, roles, entitlements, and access assignments; then detect common IAM data-quality and governance issues.  
**Environment:** Local computer + optional read-only review in a Microsoft Entra lab tenant  
**Dependencies:** Python 3.10+ (standard library only)

## Scenario

Northstar Demo is a fictional company. HR provides identity records, IAM maintains a role catalogue, and application access is granted through role assignments. Your job is to review the data before it is used for provisioning.

All records are fictional. Do not use real employee data, production credentials, or employer exports in this project.

## What you will learn

- Identity vs. account vs. credential
- Authentication vs. authorization
- Role vs. entitlement vs. assignment
- Joiner–mover–leaver lifecycle concepts
- Least privilege and why access needs a business justification
- How to validate identity and access data before automating changes

## Project structure

```text
lab-01-identity-foundations/
├── README.md
├── data/
│   ├── identities.csv
│   ├── roles.csv
│   └── role_assignments.csv
├── scripts/
│   └── validate_iam_data.py
├── diagrams/
│   └── identity-access-flow.mmd
└── evidence/
    └── README.md
```

## Step 1 — Check your local environment

Open PowerShell or Terminal and run:

```powershell
python --version
```

If your system uses the Windows Python launcher, this may work instead:

```powershell
py --version
```

Use Python 3.10 or later. If neither command works, install Python from https://www.python.org/downloads/ and select **Add Python to PATH** in the Windows installer. Reopen the terminal after installation.

## Step 2 — Understand the three data files

- `identities.csv`: fictional people and their employment/lifecycle status.
- `roles.csv`: business roles and the entitlements each role grants.
- `role_assignments.csv`: the role-to-identity assignments currently recorded.

A role is a convenient bundle of access. An entitlement is a specific permission in a target system. An assignment says that an identity has been granted a role. A role assignment is not proof by itself that the access is still appropriate; it must be checked against employment status, role policy, approvals, and business need.

## Step 3 — Run the validator

From the project folder, run:

```powershell
python scripts/validate_iam_data.py
```

Or, if needed:

```powershell
py scripts/validate_iam_data.py
```

The first run is expected to report problems. That is intentional: the data is seeded with issues for you to investigate. The script only reads CSVs and prints findings; it does not create, modify, or delete accounts or access.

## Step 4 — Investigate before changing anything

For every finding, answer:

1. Which identity or assignment is affected?
2. What control or policy might be violated?
3. What evidence would you verify before removing or granting access?
4. Who should approve the correction (for example, the manager, application owner, HR, or IAM owner)?
5. What audit evidence should be retained?

Do not automatically remove access just because a script flags it. Treat the result as a lead for investigation. Real environments may have approved cross-department access or special lifecycle rules.

## Step 5 — Remediate the mock data

Edit the CSV files in a spreadsheet editor or text editor. Save them as CSV (comma-delimited), not as `.xlsx`.

Your goal is to resolve the seeded issues without weakening the controls:

- every assignment references an existing identity and role;
- terminated identities do not retain active role assignments;
- active identities do not have end dates in the past;
- department-restricted roles are assigned only in accordance with this lab's simple policy;
- duplicate assignments are removed.

Re-run the validator after each change. A clean result should say that no validation issues were found.

## Step 6 — Optional cloud connection: observe, do not modify

In your own lab tenant only, open the Microsoft Entra admin center: https://entra.microsoft.com/

Look for the concepts represented in the files:

- Users: identity objects
- Groups and app-role assignments: ways access can be organized and granted
- Enterprise applications: applications represented in the tenant
- Audit logs: recorded changes to identities, groups, apps, and other resources
- Sign-in logs: authentication activity
- Provisioning logs: provisioning-service activity, where available

For this first lab, observe only. Do not modify a work tenant or grant privileged permissions. Portal names and features visible to you depend on tenant role and licensing.

## Step 7 — Capture GitHub evidence

Use `evidence/README.md` as your checklist. Good evidence includes:

- a screenshot of the initial validation findings;
- a screenshot of the clean validation result after remediation;
- a simple architecture sketch showing HR/source → IAM process → directory/applications;
- a short explanation of two findings and the approval/evidence needed to remediate them.

Never upload real personal data, access tokens, passwords, client secrets, tenant-sensitive screenshots, or confidential employer information.

## Definition of done

- [ ] I can explain identity, account, credential, role, entitlement, and role assignment.
- [ ] I can explain authentication vs. authorization.
- [ ] I ran the validator successfully.
- [ ] I investigated each finding before editing the mock data.
- [ ] The validator returns zero findings after remediation.
- [ ] I documented what I changed and what evidence I would retain.
- [ ] I completed the interview challenge in the main lab guide/chat.

## Interview challenge

A former contractor's account is disabled, but the identity still has an assigned role in an application. What would you verify, what would you change, who would you involve, and how would you prove the access was removed?
