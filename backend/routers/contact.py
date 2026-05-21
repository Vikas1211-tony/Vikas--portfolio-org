from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str = "Portfolio contact"
    message: str


def send_email(msg: ContactMessage):
    """Send contact form submission to your inbox via SMTP."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    to_email  = os.getenv("TO_EMAIL", "vikasmadgula123@gmail.com")

    if not smtp_user or not smtp_pass:
        # No SMTP configured — log and skip (won't crash the endpoint)
        print(f"[contact] No SMTP configured. From: {msg.email} | {msg.subject}")
        return

    email = MIMEMultipart("alternative")
    email["Subject"] = f"[Portfolio] {msg.subject}"
    email["From"]    = smtp_user
    email["To"]      = to_email
    email["Reply-To"] = msg.email

    body = f"""
New portfolio contact from {msg.name} ({msg.email})

Subject: {msg.subject}

{msg.message}
"""
    html = f"""
<h2>New portfolio contact</h2>
<p><strong>From:</strong> {msg.name} — <a href="mailto:{msg.email}">{msg.email}</a></p>
<p><strong>Subject:</strong> {msg.subject}</p>
<hr/>
<p>{msg.message.replace(chr(10), '<br/>')}</p>
"""
    email.attach(MIMEText(body, "plain"))
    email.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, email.as_string())


@router.post("", status_code=200)
def submit_contact(msg: ContactMessage, background_tasks: BackgroundTasks):
    """
    Receive a contact form submission and email it in the background.
    Always returns 200 to avoid leaking whether an email was sent.
    """
    if len(msg.message) < 5:
        raise HTTPException(status_code=422, detail="Message too short.")
    if len(msg.message) > 5000:
        raise HTTPException(status_code=422, detail="Message too long.")

    background_tasks.add_task(send_email, msg)
    return {"ok": True, "message": "Thanks! I'll be in touch soon."}
