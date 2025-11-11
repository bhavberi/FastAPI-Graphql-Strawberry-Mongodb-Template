from os import getenv

from pymongo import AsyncMongoClient


# get mongodb URI and database name from environment variale
MONGO_URI = "mongodb://{}:{}@mongo:{}/".format(
    getenv("MONGO_USERNAME", default="username"),
    getenv("MONGO_PASSWORD", default="password"),
    getenv("MONGO_PORT", default="27107"),
)
MONGO_DATABASE = getenv("MONGO_DATABASE", default="samples")

# instantiate mongo client
client = AsyncMongoClient(MONGO_URI)

# get database
db = client[MONGO_DATABASE]

async def ensure_samples_index():
    try:
        indexes = await db.samples.index_information()
        if "unique_samples" in indexes:
            print("The samples index exists.")
        else:
            await db.samples.create_index(
                [("attribute2", 1)], unique=True, name="unique_samples"
            )
            print("The samples index was created.")
        print(await db.samples.index_information())
    except Exception:
        pass