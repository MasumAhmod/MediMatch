from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# =========================================================
# SYMPTOMS PAGE
# =========================================================

@router.get("/symptoms")
def symptoms_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="symptoms.html",
        context={}
    )


# =========================================================
# RESULT PAGE
# =========================================================

@router.get("/result")
def result_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={}
    )


# =========================================================
# CONTACT PAGE
# =========================================================

@router.get("/contact")
def contact_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={}
    )