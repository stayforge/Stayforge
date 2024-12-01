from tkinter.font import names

from fastapi import APIRouter

from api.branch.view import router as branch

router = APIRouter()

router.include_router(branch, prefix="/branch", tags=["Branch"])
