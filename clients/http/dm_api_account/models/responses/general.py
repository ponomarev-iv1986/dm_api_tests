from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

UserRole = Literal[
    "Guest",
    "Player",
    "Administrator",
    "NannyModerator",
    "RegularModerator",
    "SeniorModerator",
]


class Rating(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    enabled: bool = Field(...)
    quality: int = Field(...)
    quantity: int = Field(...)
