import os
import logging

from dotenv import load_dotenv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import resend


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

    try:

        # =================================================
        # GET ENVIRONMENT VARIABLES
        # =================================================

        resend_api_key = os.getenv("RESEND_API_KEY", "").strip()
        mail_to = os.getenv("MAIL_TO", "").strip()
        mail_from = os.getenv(
            "MAIL_FROM",
            "onboarding@resend.dev"
        ).strip()


        # =================================================
        # CHECK CONFIGURATION
        # =================================================

        if not resend_api_key:
            raise ValueError(
                "RESEND_API_KEY environment variable is not configured."
            )

        if not mail_to:
            raise ValueError(
                "MAIL_TO environment variable is not configured."
            )


        # =================================================
        # SET RESEND API KEY
        # =================================================

        resend.api_key = resend_api_key


        # =================================================
        # EMAIL SUBJECT
        # =================================================

        email_subject = f"MediMatch Contact: {subject}"


        # =================================================
        # EMAIL BODY
        # =================================================

        email_body = f"""
New message from MediMatch contact form

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

----------------------------------------
This message was sent from the MediMatch website.
"""


        # =================================================
        # SEND EMAIL
        # =================================================

        resend.Emails.send(
            {
                "from": mail_from,
                "to": [mail_to],
                "subject": email_subject,
                "text": email_body,
                "reply_to": email
            }
        )


        # =================================================
        # SUCCESS
        # =================================================

        return templates.TemplateResponse(
            request=request,
            name="contact.html",
            context={
                "success": True,
                "message": (
                    "Thank you! Your message has been sent "
                    "successfully. We will get back to you soon."
                )
            }
        )


    # =====================================================
    # ERROR
    # =====================================================

    except Exception as e:

        logging.error(
            f"Contact form email sending error: {str(e)}",
            exc_info=True
        )

        return templates.TemplateResponse(
            request=request,
            name="contact.html",
            context={
                "success": False,
                "message": (
                    "We could not send your message right now. "
                    "Please email us directly at "
                    "masumahmod332@gmail.com."
                )
            }
        )
