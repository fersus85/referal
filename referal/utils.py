from typing import Any
from dataclasses import dataclass
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Template

from referal.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email_templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def generate_referal_code_email(username: str,
                                code: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f'From {project_name}. Your referal code {username}'
    html_content = render_email_template(
        template_name="get_code.html",
        context={
            'subject': 'Referal code',
            'project_name': settings.PROJECT_NAME,
            'greeting': f' Hello {username}',
            'message': f'Referal code {code}',
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def send_email(email_to: str,
               subject: str = "",
               html_content: str = "") -> None:
    server = smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))
    print('im here2')
    server.sendmail(settings.EMAILS_FROM_EMAIL,
                    email_to,
                    msg.as_string())
    server.quit()
