import json
import strawberry

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from typing import Union, Dict, Optional
from functools import cached_property

from .models import PyObjectId, Sample, Links


# custom context class
class Context(BaseContext):
    @cached_property
    def user(self) -> Union[Dict, None]:
        if not self.request:
            return None

        user = json.loads(self.request.headers.get("user", "{}"))
        return user


# custom info type
Info = _Info[Context, RootValueType]

# serialize PyObjectId as a scalar type
PyObjectIdType = strawberry.scalar(
    PyObjectId, serialize=str, parse_value=lambda v: PyObjectId(v)
)


# Object Type for the Sub-Model
@strawberry.experimental.pydantic.type(model=Links, all_fields=True)
class LinksType:
    pass


# sample object type from pydantic model with all fields exposed
@strawberry.experimental.pydantic.type(model=Sample, all_fields=True)
class FullSampleType:
    pass


@strawberry.experimental.pydantic.type(
    model=Sample,
    fields=["attribute1", "attribute2", "usingenum", "name", "email", "links"],
)
class SimpleSampleType:
    pass


# sample query's input type from pydantic model
@strawberry.experimental.pydantic.input(
    model=Sample, fields=["id", "attribute2", "usingenum", "name", "email"]
)
class SampleQueryInput:
    attribute1: strawberry.auto


# sample mutation's input type from pydantic model
@strawberry.experimental.pydantic.input(model=Links, all_fields=True)
class LinksInput:
    pass


@strawberry.experimental.pydantic.input(model=Sample, all_fields=True)
class SampleMutationInput:
    pass
