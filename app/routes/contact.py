import os

from dotenv import load_dotenv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import cast

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
# ROUTER
# =========================================================

router = APIRouter()


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_TO = cast(str, os.getenv("MAIL_TO"))


# =========================================================
# CHECK ENVIRONMENT VARIABLES
# =========================================================

if not MAIL_USERNAME:
    raise RuntimeError(
        "MAIL_USERNAME is missing from .env"
    )

if not MAIL_PASSWORD:
    raise RuntimeError(
        "MAIL_PASSWORD is missing from .env"
    )

if not MAIL_TO:
    raise RuntimeError(
        "MAIL_TO is missing from .env"
    )


# =========================================================
# MAIL CONFIGURATION
# =========================================================

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=SecretStr(MAIL_PASSWORD),
    MAIL_FROM=MAIL_USERNAME,

    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",

    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,

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
            "success": False,
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

    # =====================================================
    # EMAIL SUBJECT
    # =====================================================

    email_subject = (
        f"MediMatch Contact: {subject}"
    )


    # =====================================================
    # EMAIL BODY
    # =====================================================

    email_body = f"""
New message from MediMatch contact form

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

--------------------------------------------------
This message was sent from the MediMatch website.
--------------------------------------------------
"""


    # =====================================================
    # CREATE EMAIL MESSAGE
    # =====================================================

    email_message = MessageSchema(
        subject=email_subject,

        recipients=[
            NameEmail(
                name="MediMatch",
                email=MAIL_TO
            )
        ],

        body=email_body,

        subtype=MessageType.plain
    )


    # =====================================================
    # SEND EMAIL
    # =====================================================

    fm = FastMail(conf)

    await fm.send_message(
        email_message
    )


    # =====================================================
    # RETURN CONTACT PAGE
    # =====================================================

    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "success": True,
            "message": (
                "Your message has been sent successfully!"
            )
        }
    )
