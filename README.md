# IT Audit Lab

Hands-on IT audit and access control automation exercises using Python.

## Project Overview

This project demonstrates a basic automated user access review using Python and CSV data.

The script reviews user access records and identifies potential access control issues based on predefined audit rules.

## Audit Objective

The objective is to identify potential access control risks, including:

- Active accounts belonging to former employees
- Potential excessive privileges
- Administrative access that may not be appropriate for the user's role

## Automated Controls

### 1. Former Employee Access Check

The script identifies users whose employment status is **Former Employee** while their account status remains **Active**.

This may indicate that access was not removed after termination.

### 2. Excessive Privilege Check

The script identifies specialist-level users with **CRM Admin** access.

This is flagged as a potential excessive privilege and should be reviewed based on the principle of least privilege.

## Files

- `users.csv` - Sample user access dataset
- `inactive_user_check.py` - Python script used to perform the automated access review

## Technologies

- Python
- CSV
- Git
- GitHub

## Disclaimer

All users and data in this repository are fictional and created solely for educational and portfolio purposes.
