import strawberry

from fastapi.encoders import jsonable_encoder

from .db import db

from .models import Sample, create_utc_time
from .otypes import Info
from .otypes import SimpleSampleType, FullSampleType, SampleMutationInput


# sample mutation
@strawberry.mutation
async def sampleMutationOne(sampleInput: SampleMutationInput) -> SimpleSampleType:
    """
    Sample Mutation One
    
    Args:
        sampleInput (otypes.SampleMutationInput): Input containing sample details.
        
    Returns:
        (otypes.SimpleSampleType): Simple sample details.
    """
    # Converting the input to pydantic model - json based
    sample = jsonable_encoder(sampleInput.to_pydantic())

    # add to database
    created_record = await db.samples.insert_one(sample)

    # query back from database
    created_sample = Sample.model_validate(
        await db.samples.find_one({"_id": created_record.inserted_id})
    )

    # Returning back json, strawberry based model response
    return SimpleSampleType.from_pydantic(created_sample)


@strawberry.mutation
async def sampleMutationTwo(
    sampleInput: SampleMutationInput, info: Info
) -> FullSampleType:
    """
    Sample Mutation Two

    Args:
        sampleInput (otypes.SampleMutationInput): Input containing sample details.
        info (otypes.Info): User metadata and cookies.

    Returns:
        (otypes.FullSampleType): Full sample details.
    """
    # Getting user context - for selective permissions
    user = info.context.user
    print(user)

    input = jsonable_encoder(sampleInput.to_pydantic())

    # update to database
    await db.samples.update_one(
        {"cid": input["_id"]},
        {"$set": {"name": "UPDATED", "attribute2": create_utc_time()}},
    )

    # query back from database
    created_sample = Sample.model_validate(
        await db.samples.find_one({"_id": input["_id"]})
    )

    return FullSampleType.from_pydantic(created_sample)


# register all mutations
mutations = [sampleMutationOne, sampleMutationTwo]
