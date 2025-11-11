import strawberry

from fastapi.encoders import jsonable_encoder
from typing import List

from .db import db

# import all models and types
from .models import Sample
from .otypes import Info
from .otypes import SimpleSampleType, FullSampleType, SampleQueryInput


# sample query
@strawberry.field
async def sampleQueryOne(sampleInput: SampleQueryInput, info: Info) -> FullSampleType:
    # Getting user context - for selective permissions
    user = info.context.user
    print("user:", user)

    # Converting the input to pydantic model - json based
    sample = jsonable_encoder(sampleInput.to_pydantic())

    # query from database
    found_sample = await db.samples.find_one({"_id": sample["_id"]})

    # handle missing sample
    if found_sample:
        found_sample = Sample.model_validate(found_sample)
        return FullSampleType.from_pydantic(found_sample)
    else:
        raise Exception("Sample not found!")


# Query Returning List of values
@strawberry.field
async def sampleQueryTwo(info: Info) -> List[SimpleSampleType]:
    # Getting user context - for selective permissions
    user = info.context.user
    print("user:", user)

    """
    NOTE:-
    Mongo needs the collection name to end at s specifically
    """
    results = await db.samples.find().to_list(length=None)

    if results:
        samples = []
        for result in results:
            samples.append(
                SimpleSampleType.from_pydantic(Sample.model_validate(result))
            )
        return samples
    else:
        raise Exception("No Club Result Found")


# register all queries
queries = [sampleQueryOne, sampleQueryTwo]
