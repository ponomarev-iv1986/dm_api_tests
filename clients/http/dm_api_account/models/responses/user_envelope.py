from datetime import datetime
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from clients.http.dm_api_account.models.responses.general import Rating, UserRole


class Resource(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    roles: list[UserRole] = Field(...)
    medium_picture_url: Optional[str] = Field(None, validation_alias="mediumPictureUrl")
    small_picture_url: Optional[str] = Field(None, validation_alias="smallPictureUrl")
    status: Optional[str] = Field(None)
    rating: Rating = Field(...)
    online: Optional[datetime] = Field(None, strict=False)
    name: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    registration: Optional[datetime] = Field(None, strict=False)


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    resource: Resource = Field(...)
    metadata: Optional[Union[str, dict[Any, Any]]] = Field(None)
