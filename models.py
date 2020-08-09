from pydantic import BaseModel
from typing import Optional

# User models
class UserRegisterModel(BaseModel):
    username: str
    display_name: str
    messenger_url: Optional[str] = None
    password: str
    password_repeat: str

class UserLoginModel(BaseModel):
    username: str
    password: str

class UserProfileModel(BaseModel):
    username: str
    display_name: str
    img_url: Optional[str] = None
    messenger_url: Optional[str] = None

class RecommendedUserModel(UserProfileModel):
    similarity_match: int

class UserProfileUpdateModel(BaseModel):
    display_name: str
    img_url: Optional[str] = None
    messenger_url: Optional[str] = None

class UserPasswordChangeModel(BaseModel):
    old_password: Optional[str] = None
    new_password: Optional[str] = None

# track model
class TrackModel(BaseModel):
    title: str
    artist: str
