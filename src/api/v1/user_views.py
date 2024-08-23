import logging
from urllib.parse import urljoin

from applications.users.auth.schemas import JWTPairToken
from applications.users.interactors import UserInteractor

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from applications.users.models import UserModel
from applications.users.schemas.user_schemas import UserRegisterStruct
from applications.users.selectors import UserSelector

logger = logging.getLogger(__name__)

users_router = APIRouter()

#
# @users_router.post("/register", response_model=JWTPairToken, status_code=201, tags=["users"])
# async def register(
#     user_in: UserRegisterStruct,
# ):
#     """
#     Create new user.
#     """
#     if user_in.password != user_in.password_confirmation:
#         raise HTTPException(
#             status_code=400,
#             detail="Passwords do not match.",
#         )
#
#
#     try:
#         db_user = BaseUserRegister(**user_in.create_update_dict())
#     except Exception as e:
#         return JSONResponse(status_code=400, content={"error": str(e)})
#
#
#
#     data = get_jwt_pair_from_user(created_user)
#     return data
#
#
# @users_router.patch("/me", response_model=BaseRetrieveUser, status_code=200, tags=["users"])
# async def update_user_me(user_data: BaseUserUpdate, current_user: User = Depends(get_current_active_user)):
#     """
#     Update own user.
#     """
#     return await UserInteractor(current_user).update(user_data)
#
#
# @users_router.post("/email/resend-verification-link", status_code=204, tags=["users"])
# async def resend_verification_email_link(
#     current_user: User = Depends(get_current_active_user),
# ):
#     await UserInteractor(current_user).resend_verification_email_link()
#     return {}
#
#
# @users_router.get("/me", response_model=BaseRetrieveUser, status_code=200, tags=["users"])
# async def read_user_me(
#     request: Request,
#     current_user: User = Depends(get_current_active_user),
# ):
#     """
#     Get current user.
#     """
#     user_struct = BaseRetrieveUser.model_validate(current_user)
#     if user_struct.avatar:
#         user_struct.avatar = urljoin(str(request.base_url), str(user_struct.avatar))
#     return user_struct
