from flask import current_app, render_template
from flask_mail import Message

from extensions import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_reminder_email(reminder, recipient, message):
    subject = f"CareBridge reminder: {reminder.schedule.med_name}"
    sender = current_app.config["MAIL_DEFAULT_SENDER"]
    recipients = [recipient] if recipient else []
    text_body = render_template("email/reminder.txt", reminder=reminder, message=message)
    html_body = render_template("email/reminder.html", reminder=reminder, message=message)

    if not recipients:
        print(f"[CareBridge email fallback] {message}")
        return

    try:
        send_email(
            subject=subject,
            sender=sender,
            recipients=recipients,
            text_body=text_body,
            html_body=html_body,
        )
        print(f"[CareBridge email sent] To {recipient}: {message}")
    except Exception as exc:
        print(f"[CareBridge email fallback] To {recipient}: {message}")
        print(f"[CareBridge email fallback] Mail delivery failed: {exc}")
