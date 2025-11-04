from pydantic import BaseModel, ConfigDict, Field


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    token: str = Field(...)
    old_password: str = Field(..., serialization_alias="oldPassword")
    new_password: str = Field(..., serialization_alias="newPassword")
