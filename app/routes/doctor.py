from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


# =========================================================
# DOCTORS PAGE
# =========================================================

@router.get("/doctors")
def doctors_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="doctors.html",
        context={}
    )


# =========================================================
# DOCTOR PROFILE PAGE
# =========================================================

@router.get("/doctors/{doctor_id}")
def doctor_page(
    doctor_id: int,
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="doctor.html",
        context={
            "doctor_id": doctor_id
        }
    )