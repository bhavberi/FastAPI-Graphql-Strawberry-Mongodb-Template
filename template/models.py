import strawberry
from bson import ObjectId
from datetime import datetime
from enum import Enum
from pydantic import (
    field_validator,
    ConfigDict,
    BaseModel,
    Field,
    EmailStr,
    AnyHttpUrl,
    ValidationInfo,
)
from pydantic_core import core_schema
from typing import Any, List
from pytz import timezone


# for handling mongo ObjectIds
class PyObjectId(ObjectId):
    """
    Class for handling MongoDB document ObjectIds for 'id' fields in Models.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


# Custom Function based Validator
def gmail_only(v: str) -> str:
    """
    Validator to allow only Gmail emails.

    Args:
        v (str): Email string to be validated.

    Raises:
        ValueError: If email is not a valid Gmail email.

    Returns:
        (str): Valid Gmail email.
    """
    valid_domains = ["@gmail.com", "@google.com", "@google.in"]
    if any(valid_domain in v for valid_domain in valid_domains):
        return v.lower()

    raise ValueError("Gmail emails only.")


# Function for generating default values in model in Default Factory
def current_year() -> int:
    """Returns the current year."""
    return datetime.now().year

# Function for generating UTC time
def create_utc_time():
    """
    Returns the current time according to UTC timezone.
    """
    return datetime.now(timezone("UTC"))


# Enum Type for Model - fixed range of values
@strawberry.enum
class EnumTrial(str, Enum):
    """Enum for trialing enum field in Model."""
    online = "online"
    offline = "offline"
    hybrid = "hybrid"


# Sub-Class for Pydantic Model
class Links(BaseModel):
    """
    Sub-model for holding links.
    
    Attributes:
        linkone (AnyHttpUrl | None): First link (Required).
        linktwo (AnyHttpUrl | None): Second link (Optional)."""
    linkone: AnyHttpUrl | None = Field(...)
    linktwo: AnyHttpUrl | None = Field(None)


# Sample Pydantic Model
class Sample(BaseModel):
    """
    Sample Pydantic Model for demonstration.

    Attributes:
        id (PyObjectId): MongoDB ObjectId for the model.
        attribute1 (str | None): Optional attribute with default value.
        attribute2 (str): Required attribute.
        boolean (bool): Required boolean with default factory.
        usingenum (EnumTrial): Enum field with default value.
        listnum (List[int] | None): Optional list of integers.
        links (Links | None): Optional sub-model for links.
        date_time (datetime): Required datetime with default factory.
        name (str): Required name with length constraints.
        email (EmailStr): Required email field.
        contact (str | None): Optional contact field with regex validation.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # Model id

    # Optional and auto generated if not specified
    attribute1: str | None = Field(
        "Default", description="Atrribute 1"
    )
    attribute2: str = Field(..., description="Attribute 2")  # Required always

    # Required & auto-generated, if not specified
    boolean: bool = Field(default_factory=(lambda: 0 == 1))
    # Enum type - required and having a default value
    usingenum: EnumTrial = EnumTrial.hybrid
    listnum: List[int] | None = Field(None)  # List of values
    links: Links | None = Field(None)  # Using a sub-model

    # datetime type, auto-generated & required
    date_time: datetime = Field(default_factory=datetime.utcnow)

    # Required always with constraints (Can use constr too)
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)  # Optional but required always

    # Optional, validation using regex
    contact: str | None = Field(
        None,
        pattern=r"((\+91)|(0))?(-)?\s*?(91)?\s*?([6-9]{1}\d{2})((-?\s*?(\d{3})-?\s*?(\d{4}))|((\d{2})-?\s*?(\d{5})))",
    )

    # Validators

    @field_validator("name", mode="before")
    # Value - the field for which validator, values - all other field values
    def check_name(cls, value, info: ValidationInfo):
        if value == info.data["attribute2"]:
            return value.lower()
        return value.upper()

    # Would query only when field is accessed via the model
    @field_validator("attribute1")
    @classmethod
    def check_attribute1(cls, value):
        if "z" in value:
            return value * 2
        return value
    
    @field_validator("email", mode="before")
    def _check_email(cls, v):
        return gmail_only(v)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        str_strip_whitespace=True,
        str_max_length=200,
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
        extra="forbid",
    )
