import json
import strawberry

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from typing import Union, Dict
from functools import cached_property

from .models import PyObjectId, Sample, Links


# custom context class
class Context(BaseContext):
    """
    Class provides user metadata and cookies from request headers, has
    methods for doing this.
    """

    @cached_property
    def user(self) -> Union[Dict, None]:
        if not self.request:
            return None

        user = json.loads(self.request.headers.get("user", "{}"))
        return user

    @cached_property
    def cookies(self) -> Union[Dict, None]:
        if not self.request:
            return None

        cookies = json.loads(self.request.headers.get("cookies", "{}"))
        return cookies


# custom info type
Info = _Info[Context, RootValueType]
"""custom info Type for user metadata"""

# serialize PyObjectId as a scalar type
PyObjectIdType = strawberry.scalar(
    PyObjectId, serialize=str, parse_value=lambda v: PyObjectId(v)
)
"""A scalar Type for serializing PyObjectId, used for id field"""


# Object Type for the Sub-Model
@strawberry.experimental.pydantic.type(model=Links, all_fields=True)
class LinksType:
    """
    Type used for return of links.

    Attributes:
        linkone (str): First link.
        linktwo (str): Second link.
    """
    pass


# sample object type from pydantic model with all fields exposed
@strawberry.experimental.pydantic.type(model=Sample, all_fields=True)
class FullSampleType:
    """
    Full Type for Sample model with all fields.

    Attributes:
        id (PyObjectIdType): MongoDB ObjectId for the model.
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
    pass


@strawberry.experimental.pydantic.type(
    model=Sample,
    fields=["attribute1", "attribute2", "usingenum", "name", "email", "links"],
)
class SimpleSampleType:
    """
    Simple Type for Sample model with selected fields.

    Attributes:
        attribute1 (str | None): Optional attribute with default value.
        attribute2 (str): Required attribute.
        usingenum (EnumTrial): Enum field with default value.
        name (str): Required name with length constraints.
        email (EmailStr): Required email field.
        links (Links | None): Optional sub-model for links.
    """
    pass


# sample query's input type from pydantic model
@strawberry.experimental.pydantic.input(
    model=Sample, fields=["id", "attribute2", "usingenum", "name", "email"]
)
class SampleQueryInput:
    """
    Input Type for Sample model used in queries.

    Attributes:
        id (PyObjectIdType): MongoDB ObjectId for the model.
        attribute2 (str): Required attribute.
        usingenum (EnumTrial): Enum field with default value.
        name (str): Required name with length constraints.
        email (EmailStr): Required email field.
    """
    attribute1: strawberry.auto


# sample mutation's input type from pydantic model
@strawberry.experimental.pydantic.input(model=Links, all_fields=True)
class LinksInput:
    """
    Input used for input of links.

    Attributes:
        linkone (str): First link.
        linktwo (str): Second link.
    """
    pass


@strawberry.experimental.pydantic.input(model=Sample, all_fields=True)
class SampleMutationInput:
    """
    Input Type for Sample model used in mutations.

    Attributes:
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
    pass
