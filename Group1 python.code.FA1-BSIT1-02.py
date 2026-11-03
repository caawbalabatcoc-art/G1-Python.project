
from datetime import datetime
import re

accounts = [
    {
        "full_name": "Module Distributor",
        "student_id": None,
        "username": "admin",
        "password": "admin123",
        "role": "Module Distributor"
    }
]

requests = []
schedules = []
claim_records = []

MODULES = ["ITE 260", "ITE 366"]
MAX_STUDENTS = 199


def validate_student_id():
    while True:
        student_id = input(
            "Student ID (XX-XXXX-XXXXXX): "
        ).strip()

        if re.fullmatch(r"\d{2}-\d{4}-\d{6}", student_id):
            return student_id

        print("Invalid Student ID format.")
        print("Example: 02-2425-008111")


def find_student(student_id):
    for account in accounts:
        if (
            account["role"] == "Student"
            and account["student_id"] == student_id
        ):
            return account
    return None


def find_account(username):
    for account in accounts:
        if account["username"] == username:
            return account
    return None


def find_request(student_id, module):
    for request in requests:
        if (
            request["student_id"] == student_id
            and request["module"] == module
        ):
            return request
    return None


def find_schedule(student_id, module):
    for schedule in schedules:
        if (
            schedule["student_id"] == student_id
            and schedule["module"] == module
        ):
            return schedule
    return None


def validate_future_datetime():
    while True:
        date_input = input(
            "Distribution Date (YYYY-MM-DD): "
        ).strip()

        try:
            distribution_date = datetime.strptime(
                date_input, "%Y-%m-%d"
            )
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            continue

        if distribution_date.year < 2026:
            print("The distribution year must be 2026 or later.")
            continue

        time_input = input(
            "Distribution Time (HH:MM AM/PM): "
        ).strip().upper()

        try:
            distribution_time = datetime.strptime(
                time_input, "%I:%M %p"
            )
        except ValueError:
            print("Invalid time. Example: 08:00 AM or 04:00 PM.")
            continue

        start_time = datetime.strptime(
            "08:00 AM", "%I:%M %p"
        ).time()

        end_time = datetime.strptime(
            "04:00 PM", "%I:%M %p"
        ).time()

        if not start_time <= distribution_time.time() <= end_time:
            print("Distribution time must be between 8:00 AM and 4:00 PM.")
            continue

        combined_datetime = datetime.strptime(
            date_input + " " + time_input,
            "%Y-%m-%d %I:%M %p"
        )

        if combined_datetime <= datetime.now():
            print("The distribution date and time must be in the future.")
            continue

        return date_input, distribution_time.strftime("%I:%M %p")


def register_student():
    print("\nSTUDENT REGISTRATION")

    registered_students = sum(
        1 for account in accounts
        if account["role"] == "Student"
    )

    if registered_students >= MAX_STUDENTS:
        print("Registration closed. The student limit has been reached.")
        return

    full_name = input("Full Name: ").strip()

    if not full_name:
        print("Full name is required.")
        return

    student_id = validate_student_id()

    if find_student(student_id):
        print("This Student ID is already registered.")
        return

    username = input("Create Username: ").strip()

    if not username:
        print("Username is required.")
        return

    if find_account(username):
        print("Username already exists.")
        return

    password = input("Create Password: ")

    if not password:
        print("Password is required.")
        return

    accounts.append({
        "full_name": full_name,
        "student_id": student_id,
        "username": username,
        "password": password,
        "role": "Student"
    })

    print("\nStudent registration completed successfully.")
    print("Registered students:", registered_students + 1)
    print("Remaining slots:", MAX_STUDENTS - registered_students - 1)
    print("You may now log in.")


def login():
    print("\nLOGIN")

    username = input("Username: ").strip()
    password = input("Password: ")

    account = find_account(username)

    if account is None or account["password"] != password:
        print("Invalid username or password.")
        return

    print("\nLogin successful!")
    print("Welcome, " + account["full_name"] + ".")

    if account["role"] == "Student":
        student_menu(account)
    elif account["role"] == "Module Distributor":
        distributor_menu()


def request_modules(student):
    print("\nREQUEST MODULES")

    student_id = student["student_id"]

    student_requests = [
        request for request in requests
        if request["student_id"] == student_id
    ]

    if len(student_requests) >= len(MODULES):
        print("You have already requested all available modules.")
        return

    print("Available Modules:")
    print("1. ITE 260")
    print("2. ITE 366")
    print("0. Finish Requesting")

    while len(student_requests) < len(MODULES):
        choice = input("Select a module: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            module = "ITE 260"
        elif choice == "2":
            module = "ITE 366"
        else:
            print("Invalid choice. Select 1, 2, or 0.")
            continue

        if find_request(student_id, module):
            print("You have already requested this module.")
            continue

        new_request = {
            "student_id": student_id,
            "full_name": student["full_name"],
            "module": module
        }

        requests.append(new_request)
        student_requests.append(new_request)

        print(module + " requested successfully.")

        if len(student_requests) < len(MODULES):
            another = input(
                "Request another module? (yes/no): "
            ).strip().lower()

            if another != "yes":
                break

    print("\nModule request process completed.")


def view_student_schedules(student):
    print("\nMY DISTRIBUTION SCHEDULES")

    student_id = student["student_id"]

    student_requests = [
        request for request in requests
        if request["student_id"] == student_id
    ]

    if not student_requests:
        print("You have not requested any modules.")
        return

    for request in student_requests:
        print("\nModule:", request["module"])

        schedule = find_schedule(student_id, request["module"])

        if schedule:
            print("Distribution Date:", schedule["date"])
            print("Distribution Time:", schedule["time"])
            print(
                "Claim Status:",
                "Claimed" if schedule["claimed"] else "Not yet claimed"
            )
        else:
            print("Status: Waiting for distribution schedule")


def student_menu(student):
    while True:
        print("\nSTUDENT MENU")
        print("1. Request Modules")
        print("2. View My Distribution Schedules")
        print("3. Log Out")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            request_modules(student)
        elif choice == "2":
            view_student_schedules(student)
        elif choice == "3":
            print("You have logged out.")
            break
        else:
            print("Invalid choice. Please try again.")


def add_schedule():
    print("\nADD DISTRIBUTION SCHEDULE")

    student_id = validate_student_id()
    student = find_student(student_id)

    if student is None:
        print("Student not found. Register the student first.")
        return

    student_requests = [
        request for request in requests
        if request["student_id"] == student_id
    ]

    if not student_requests:
        print("This student has not requested any modules.")
        return

    print("\nStudent Name:", student["full_name"])
    print("Student ID:", student_id)
    print("\nRequested Modules:")

    available_modules = []

    for request in student_requests:
        module = request["module"]

        if find_schedule(student_id, module):
            print(module + " - Schedule already assigned")
        else:
            available_modules.append(module)
            print(f"{len(available_modules)}. {module}")

    if not available_modules:
        print("All requested modules already have schedules.")
        return

    while True:
        choice = input("Select module to schedule: ").strip()

        if choice.isdigit():
            choice_number = int(choice)

            if 1 <= choice_number <= len(available_modules):
                module = available_modules[choice_number - 1]
                break

        print("Invalid choice. Select an available module number.")

    date, time = validate_future_datetime()

    schedules.append({
        "student_id": student_id,
        "full_name": student["full_name"],
        "module": module,
        "date": date,
        "time": time,
        "claimed": False,
        "claimed_at": None
    })

    print("\nDistribution schedule added successfully.")
    print("Student:", student["full_name"])
    print("Module:", module)
    print("Distribution Date:", date)
    print("Distribution Time:", time)


def view_schedules():
    print("\nDISTRIBUTION SCHEDULES")

    if not schedules:
        print("No distribution schedules available.")
        return

    print(
        f"\n{'No.':<5}{'Student Name':<25}{'Student ID':<18}"
        f"{'Module':<12}{'Date':<14}{'Time':<12}{'Claim Status'}"
    )
    print("-" * 105)

    for number, schedule in enumerate(schedules, start=1):
        status = "Claimed" if schedule["claimed"] else "Not Claimed"

        print(
            f"{number:<5}{schedule['full_name']:<25}"
            f"{schedule['student_id']:<18}{schedule['module']:<12}"
            f"{schedule['date']:<14}{schedule['time']:<12}{status}"
        )


def claim_module():
    print("\nRECORD MODULE CLAIM")

    student_id = validate_student_id()
    student = find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    student_schedules = [
        schedule for schedule in schedules
        if schedule["student_id"] == student_id
    ]

    if not student_schedules:
        print("This student has no distribution schedules.")
        return

    print("\nStudent Name:", student["full_name"])
    print("Student ID:", student_id)
    print("\nScheduled Modules:")

    for number, schedule in enumerate(student_schedules, start=1):
        status = "Claimed" if schedule["claimed"] else "Not Claimed"

        print(
            f"{number}. {schedule['module']} | "
            f"{schedule['date']} at {schedule['time']} | {status}"
        )

    while True:
        choice = input(
            "Select module to record as claimed (0 to cancel): "
        ).strip()

        if choice == "0":
            print("Claim recording cancelled.")
            return

        if choice.isdigit():
            choice_number = int(choice)

            if 1 <= choice_number <= len(student_schedules):
                schedule = student_schedules[choice_number - 1]
                break

        print("Invalid choice. Select a listed module or 0.")

    if schedule["claimed"]:
        print("This module has already been recorded as claimed.")
        return

    confirmation = input(
        "Confirm that the student received the module? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Claim recording cancelled.")
        return

    claimed_at = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    schedule["claimed"] = True
    schedule["claimed_at"] = claimed_at

    claim_records.append({
        "student_id": student_id,
        "full_name": student["full_name"],
        "module": schedule["module"],
        "distribution_date": schedule["date"],
        "distribution_time": schedule["time"],
        "claimed_at": claimed_at
    })

    print("\nModule claim recorded successfully.")
    print("Student:", student["full_name"])
    print("Student ID:", student_id)
    print("Module:", schedule["module"])
    print("Claim Date and Time:", claimed_at)


def view_claim_records():
    print("\nTABLE OF STUDENTS WHO CLAIMED MODULES")

    if not claim_records:
        print("No module claims have been recorded.")
        return

    print(
        f"\n{'No.':<5}{'Student Name':<25}{'Student ID':<18}"
        f"{'Module':<12}{'Distribution Date':<20}"
        f"{'Distribution Time':<20}{'Claimed At'}"
    )
    print("-" * 125)

    for number, record in enumerate(claim_records, start=1):
        print(
            f"{number:<5}{record['full_name']:<25}"
            f"{record['student_id']:<18}{record['module']:<12}"
            f"{record['distribution_date']:<20}"
            f"{record['distribution_time']:<20}"
            f"{record['claimed_at']}"
        )


def reschedule_schedule():
    print("\nRESCHEDULE STUDENT")

    student_id = validate_student_id()

    student_schedules = [
        schedule for schedule in schedules
        if schedule["student_id"] == student_id
    ]

    if not student_schedules:
        print("No schedules found for this Student ID.")
        return

    print("\nExisting Schedules:")

    for number, schedule in enumerate(student_schedules, start=1):
        status = "Claimed" if schedule["claimed"] else "Not Claimed"

        print(
            f"{number}. {schedule['module']} | "
            f"{schedule['date']} at {schedule['time']} | {status}"
        )

    while True:
        choice = input(
            "Select schedule to reschedule: "
        ).strip()

        if choice.isdigit():
            choice_number = int(choice)

            if 1 <= choice_number <= len(student_schedules):
                schedule = student_schedules[choice_number - 1]
                break

        print("Invalid choice. Select a listed schedule.")

    if schedule["claimed"]:
        print("A claimed module cannot be rescheduled.")
        return

    print("\nStudent Name:", schedule["full_name"])
    print("Module:", schedule["module"])
    print("Current Date:", schedule["date"])
    print("Current Time:", schedule["time"])

    print("\nEnter the New Distribution Schedule.")

    new_date, new_time = validate_future_datetime()

    schedule["date"] = new_date
    schedule["time"] = new_time

    print("\nSchedule rescheduled successfully.")
    print("New Distribution Date:", new_date)
    print("New Distribution Time:", new_time)


def distributor_menu():
    while True:
        print("\nMODULE DISTRIBUTOR MENU")
        print("1. Add Distribution Schedule")
        print("2. View Distribution Schedules")
        print("3. Reschedule Student")
        print("4. Record Module Claim")
        print("5. View Claimed Module Records")
        print("6. Log Out")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_schedule()
        elif choice == "2":
            view_schedules()
        elif choice == "3":
            reschedule_schedule()
        elif choice == "4":
            claim_module()
        elif choice == "5":
            view_claim_records()
        elif choice == "6":
            print("You have logged out.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    while True:
        print("\nMODULE DISTRIBUTION SCHEDULING")
        print("ITE 260 AND ITE 366 FIRST-YEAR BSIT STUDENTS")
        print("PHINMA CAGAYAN DE ORO COLLEGE")
        print("\n1. Student Registration")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
