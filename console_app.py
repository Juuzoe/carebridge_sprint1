import os
from core import load_logs, save_logs, already_logged_today, add_log

SCHEDULES = {
    1: {"med_name": "Aspirin", "dosage": "1 tablet", "time_of_day": "morning"},
    2: {"med_name": "Vitamin D", "dosage": "1 capsule", "time_of_day": "evening"},
}

LOG_FILE = os.path.join(os.path.dirname(__file__), "static", "dose_logs.json")

def print_schedules():
    print("\nMedication schedules:")
    for sid, s in SCHEDULES.items():
        print(f"  {sid}) {s['med_name']} — {s['dosage']} ({s['time_of_day']})")

def print_logs(logs):
    if not logs:
        print("\nNo actions yet.")
        return
    print("\nHistory (newest first):")
    for item in logs[:30]:
        print(f"- {item['when']} | {item['username']} | {item['med_name']} | {item['status']}")

def pick_schedule_id():
    try:
        return int(input("Enter schedule id: ").strip())
    except ValueError:
        return None

def main():
    username = input("Enter your name: ").strip()
    if not username:
        print("Name is required.")
        return

    while True:
        print("\nCareBridge (Console)")
        print("1) View schedules")
        print("2) Log TAKEN")
        print("3) Log SKIPPED")
        print("4) Remind me later")
        print("5) View history")
        print("6) Clear history")
        print("0) Exit")

        choice = input("Choose: ").strip()
        logs = load_logs(LOG_FILE)

        if choice == "1":
            print_schedules()

        elif choice in ("2", "3", "4"):
            print_schedules()
            sid = pick_schedule_id()
            if sid is None or sid not in SCHEDULES:
                print("Invalid schedule id.")
                continue

            if already_logged_today(logs, sid, username):
                print("Already logged for today (for this user).")
                continue

            if choice == "2":
                status = "taken"
            elif choice == "3":
                status = "skipped"
            else:
                status = "remind_later"

            logs = add_log(logs, sid, SCHEDULES[sid]["med_name"], username, status)
            save_logs(LOG_FILE, logs)
            print(f"Recorded: {status}")

        elif choice == "5":
            print_logs(logs)

        elif choice == "6":
            save_logs(LOG_FILE, [])
            print("History cleared.")

        elif choice == "0":
            break

        else:
            print("Unknown option.")

if __name__ == "__main__":
    main()
