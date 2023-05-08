import logging
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from jinja2 import Template
from jose import JWTError, jwt
from src.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_content: str = "",
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = email_to
    msg["Subject"] = subject_template
    msg.attach(MIMEText(html_content, "html"))
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        response = smtp.sendmail(msg["From"], msg["To"], msg.as_string())
        # ! need to log responses to a file
        logging.info(response)


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template = Template(f.read())

    html_content = template.render(project_name=project_name, email=email_to)
    send_email(email_to=email_to, subject_template=subject, html_content=html_content)


def send_new_account_email(email: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template = Template(f.read())

    link = f"{settings.SERVER_HOST}/login"
    html_content = template.render(project_name=project_name, username=email, password=password, link=link)
    send_email(email_to=email, subject_template=subject, html_content=html_content)


def send_magic_link_email(email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Magic Link {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "magic_link.html") as f:
        template = Template(f.read())

    server_host = settings.SERVER_HOST
    link = f"{server_host}/magic-link?token={token}"

    html_content = template.render(
        project_name=project_name, email=email, valid_hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS, link=link
    )
    send_email(email_to=email, subject_template=subject, html_content=html_content)


def generate_magic_link_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_magic_link_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except JWTError:
        return None
