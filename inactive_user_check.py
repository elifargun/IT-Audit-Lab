import csv

with open("users.csv", newline="", encoding="utf-8") as file:
    users = csv.DictReader(file)

    for user in users:
        if user["employment_status"] == "Former Employee" and user["status"] == "Active":
            print(user["name"])
