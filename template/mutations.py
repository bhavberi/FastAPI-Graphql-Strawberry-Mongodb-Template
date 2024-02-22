import strawberry

from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

from .db import db

from .models import Sample
from .otypes import Info
from .otypes import SimpleSampleType, FullSampleType, SampleMutationInput


# sample mutation
@strawberry.mutation
def sampleMutationOne(sampleInput: SampleMutationInput) -> SimpleSampleType:
    sample = jsonable_encoder(sampleInput.to_pydantic())  # type: ignore
    # Converting the input to pydantic model - json based

    # add to database
    created_id = db.samples.insert_one(sample).inserted_id

    # query back from database
    created_sample = Sample.parse_obj(db.samples.find_one({"_id": created_id}))

    # Returning back json, strawberry based model response
    return SimpleSampleType.from_pydantic(created_sample)  # type: ignore


@strawberry.mutation
def sampleMutationTwo(sampleInput: SampleMutationInput, info: Info) -> FullSampleType:
    user = info.context.user
    print(user)
    # Getting user context - for selective permissions

    input = jsonable_encoder(sampleInput.to_pydantic())  # type: ignore

    # update to database
    db.samples.update_one(
        {"cid": input["_id"]},
        {"$set": {"name": "UPDATED", "attribute2": str(datetime.utcnow)}},
    )

    # query back from database
    created_sample = Sample.parse_obj(db.samples.find_one({"_id": input["_id"]}))

    return FullSampleType.from_pydantic(created_sample)  # type: ignore


# register all mutations
mutations = [sampleMutationOne, sampleMutationTwo]
