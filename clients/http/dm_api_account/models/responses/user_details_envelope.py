from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from clients.http.dm_api_account.models.responses.general import Rating, UserRole

BbParseMode = Literal["Common", "Info", "Post", "Chat"]

ColorShema = Literal["Modern", "Pale", "Classic", "ClassicPale", "Night"]


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    value: str
    parse_mode: BbParseMode = Field(..., validation_alias="parseMode")


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    posts_per_page: int = Field(..., validation_alias="postsPerPage")
    comments_per_page: int = Field(..., validation_alias="commentsPerPage")
    topics_per_page: int = Field(..., validation_alias="topicsPerPage")
    messages_per_page: int = Field(..., validation_alias="messagesPerPage")
    entities_per_page: int = Field(..., validation_alias="entitiesPerPage")


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    color_schema: ColorShema = Field(..., validation_alias="colorSchema")
    nanny_greetings_message: Optional[str] = Field(
        None, validation_alias="nannyGreetingsMessage"
    )
    paging: PagingSettings = Field(...)


class UserDetails(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    login: str = Field(...)
    roles: list[UserRole] = Field(...)
    medium_picture_url: Optional[str] = Field(None, validation_alias="mediumPictureUrl")
    small_picture_url: Optional[str] = Field(None, validation_alias="smallPictureUrl")
    status: Optional[str] = Field(None)
    rating: Rating = Field(...)
    online: datetime = Field(..., strict=False)
    name: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    registration: datetime = Field(..., strict=False)
    icq: Optional[str] = Field(None)
    skype: Optional[str] = Field(None)
    original_picture_url: Optional[str] = Field(
        None, validation_alias="originalPictureUrl"
    )
    info: Union[InfoBbText, str] = Field(...)
    settings: UserSettings = Field(...)


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    resource: UserDetails = Field(...)
    metadata: Optional[str] = Field(None)
