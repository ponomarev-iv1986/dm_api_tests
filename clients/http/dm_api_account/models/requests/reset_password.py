from pydantic import BaseModel, ConfigDict, Field


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    email: str = Field(...)
