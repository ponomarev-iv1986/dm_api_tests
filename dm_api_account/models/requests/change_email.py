from pydantic import BaseModel, ConfigDict, Field


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)
