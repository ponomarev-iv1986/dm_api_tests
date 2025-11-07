from pydantic import BaseModel, ConfigDict, Field


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
