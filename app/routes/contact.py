import os
import logging
from dotenv import load_dotenv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType,
    NameEmail,
)
from pydantic import SecretStr

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

# =========================================================
# ROUTER & TEMPLATES
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

# =========================================================
# MAIL CONFIGURATION HELPER
# =========================================================

def get_mail_config() -> ConnectionConfig:
    mail_username = os.getenv("MAIL_USERNAME", "").strip()
    mail_password = os.getenv("MAIL_PASSWORD", "").strip()
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_ssl = os.getenv("MAIL_SSL_TLS", "false").lower() in ("true", "1", "yes")
    mail_starttls = os.getenv("MAIL_STARTTLS", "true" if not mail_ssl else "false").lower() in ("true", "1", "yes")

    if not mail_username or not mail_password:
        raise ValueError("MAIL_USERNAME and MAIL_PASSWORD environment variables are required.")

    return ConnectionConfig(
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=SecretStr(mail_password),
        MAIL_FROM=mail_username,
        MAIL_PORT=mail_port,
        MAIL_SERVER=mail_server,
        MAIL_STARTTLS=mail_starttls,
        MAIL_SSL_TLS=mail_ssl,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )


# =========================================================
# CONTACT PAGE - GET
# =========================================================

@router.get(
    "/contact",
    response_class=HTMLResponse
)
async def contact_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "success": None,
            "message": None
        }
    )


# =========================================================
# CONTACT PAGE - POST
# =========================================================

@router.post(
    "/contact",
    response_class=HTMLResponse
)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    mail_to = os.getenv("MAIL_TO", os.getenv("MAIL_USERNAME", "")).strip()

    try:
        conf = get_mail_config()

        if not mail_to:
            raise ValueError("MAIL_TO recipient email is not configured.")

        email_subject = f"MediMatch Contact: {subject}"
        email_body = f"""New message from MediMatch contact form

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the MediMatch website.
"""

        email_message = MessageSchema(
            subject=email_subject,
            recipients=[
                NameEmail(
                    name="MediMatch Admin",
                    email=mail_to
                )
            ],
            body=email_body,
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        await fm.send_message(email_message)

        return templates.TemplateResponse(
            request=request,
            name="contact.html",
            context={
                "success": True,
                "message": "Thank you! Your message has been sent successfully. We will get back to you soon."
            }
        )

    except Exception as e:
        logging.error(f"Contact form email sending error: {str(e)}", exc_info=True)

        return templates.TemplateResponse(
            request=request,
            name="contact.html",
            context={
                "success": False,
                "message": "We could not send your message right now due to a mail server error. Please email us directly at masumahmod332@gmail.com."
            }
        )