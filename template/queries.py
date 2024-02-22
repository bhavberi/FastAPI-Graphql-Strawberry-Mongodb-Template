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
def sampleQueryOne(sampleInput: SampleQueryInput, info: Info) -> FullSampleType:
    user = info.context.user
    print("user:", user)
    # Getting user context - for selective permissions

    sample = jsonable_encoder(sampleInput.to_pydantic())  # type: ignore
    # Converting the input to pydantic model - json based

    # query from database
    found_sample = db.samples.find_one({"_id": sample["_id"]})

    # handle missing sample
    if found_sample:
        found_sample = Sample.parse_obj(found_sample)
        return FullSampleType.from_pydantic(found_sample)  # type: ignore
    else:
        raise Exception("Sample not found!")


# Query Returning List of values
@strawberry.field
def sampleQueryTwo(info: Info) -> List[SimpleSampleType]:
    user = info.context.user
    print("user:", user)
    # Getting user context - for selective permissions

    results = db.samples.find()
    """
    NOTE:-
    Mongo needs the collection name to end at s specifically
    """

    if results:
        samples = []
        for result in results:
            samples.append(SimpleSampleType.from_pydantic(Sample.parse_obj(result)))  # type: ignore
        return samples
    else:
        raise Exception("No Club Result Found")


# register all queries
queries = [sampleQueryOne, sampleQueryTwo]
