import os
from flask import Flask, render_template, redirect, url_for, flash, session
from forms import ConfirmDoseForm
from core import load_logs, save_logs, already_logged_today, add_log

# so i think we will add data bases in sprint 2 cus even though i know sql or mongro its better not to rush lol
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"

SCHEDULES = {
    1: {"med_name": "Aspirin", "dosage": "1 tablet", "time_of_day": "morning"},
    2: {"med_name": "Vitamin D", "dosage": "1 capsule", "time_of_day": "evening"},
}

LOG_FILE = os.path.join(app.root_path, "static", "dose_logs.json")

@app.route("/")
def home():
    return render_template("home.html", schedules=SCHEDULES)

@app.route("/reminder/<int:schedule_id>", methods=["GET", "POST"])
def reminder(schedule_id: int):
    sched = SCHEDULES.get(schedule_id)
    if not sched:
        flash("Schedule not found.")
        return redirect(url_for("home"))

    form = ConfirmDoseForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        session["username"] = username

        if form.taken.data:
            status = "taken"
        elif form.skipped.data:
            status = "skipped"
        else:
            status = "remind_later"

        logs = load_logs(LOG_FILE)

        if already_logged_today(logs, schedule_id, username):
            flash("Already logged for today (for this user).")
            return redirect(url_for("history"))

        logs = add_log(logs, schedule_id, sched["med_name"], username, status)
        save_logs(LOG_FILE, logs)

        if status == "taken":
            flash("Recorded: Taken.")
        elif status == "skipped":
            flash("Recorded: Skipped.")
        else:
            flash("Recorded: Remind me later. (Prototype: no real timer)")

        return redirect(url_for("history"))

    if "username" in session:
        form.username.data = session["username"]

    return render_template("reminder.html", sched=sched, schedule_id=schedule_id, form=form)

@app.route("/history")
def history():
    logs = load_logs(LOG_FILE)
    return render_template("history.html", logs=logs)

@app.route("/history/clear")
def clear_history():
    save_logs(LOG_FILE, [])
    flash("History cleared.")
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(debug=True)
