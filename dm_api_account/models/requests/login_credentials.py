from pydantic import BaseModel, ConfigDict, Field


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    password: str = Field(...)
    remember_me: bool = Field(..., serialization_alias="rememberMe")
