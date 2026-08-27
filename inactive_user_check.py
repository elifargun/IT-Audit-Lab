import csv

with open("users.csv", newline="", encoding="utf-8") as file:
    users = csv.DictReader(file)

    for user in users:
        if user["employment_status"] == "Former Employee" and user["status"] == "Active":
            print("\nACCESS CONTROL FINDING")
            print("------------------------------")
            print("User:", user["name"])
            print("Access:", user["access"])
            print("Account Status:", user["status"])
            print("Employment Status:", user["employment_status"])
            print("Risk Level: CRITICAL")
        if user["role"] == "Specialist" and user["access"] == "CRM Admin":
            print("\nACCESS CONTROL FINDING")
            print("------------------------------")
            print("User:", user["name"])
            print("Role:", user["role"])
            print("Access:", user["access"])
            print("Finding: Potential excessive privilege")
            print("Risk Level: HIGH")