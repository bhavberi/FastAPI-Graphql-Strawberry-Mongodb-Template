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
    validator,
    ValidationInfo,
)
from pydantic_core import core_schema
from typing import Any, List


# for handling mongo ObjectIds
class PyObjectId(ObjectId):
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
    valid_domains = ["@gmail.com", "@google.com", "@google.in"]
    if any(valid_domain in v for valid_domain in valid_domains):
        return v.lower()

    raise ValueError("Gmail emails only.")


# Function for generating default values in model in Default Factory
def current_year() -> int:
    return datetime.now().year


# Enum Type for Model - fixed range of values
@strawberry.enum
class EnumTrial(str, Enum):
    online = "online"
    offline = "offline"
    hybrid = "hybrid"


# Sub-Class for Pydantic Model
class Links(BaseModel):
    linkone: AnyHttpUrl | None = Field(...)
    linktwo: AnyHttpUrl | None = Field(None)


# Sample Pydantic Model
class Sample(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # Model id

    # Optional and auto generated if not specified
    attribute1: str | None = Field(
        default_factory=lambda: "Default", description="Atrribute 1"
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
    # Allow reuse for using the same function at other places too
    _check_email = validator("email", allow_reuse=True)(gmail_only)

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
        if "a" in value:
            return value * 2
        return value

    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        str_strip_whitespace=True,
        str_max_length=200,
        validate_assignment=True,
        extra="forbid",
    )
