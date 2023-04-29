from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from src.api import deps
from src.models.json_msg import JsonMsg
from src.models.user import User
from src.utils import send_test_email

router = APIRouter()


@router.post("/test-email", response_model=JsonMsg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Test emails.
    """
    # TODO disallow users from accessing endpoint, only for testing
    send_test_email(email_to=email_to)
    return {"message": "Test email sent"}
