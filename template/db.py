from os import getenv

from pymongo import MongoClient


# get mongodb URI and database name from environment variale
MONGO_URI = "mongodb://{}:{}@mongo:{}/".format(
    getenv("MONGO_USERNAME", default="username"),
    getenv("MONGO_PASSWORD", default="password"),
    getenv("MONGO_PORT", default="27107"),
)
MONGO_DATABASE = getenv("MONGO_DATABASE", default="samples")

# instantiate mongo client
client = MongoClient(MONGO_URI)

# get database
db = client[MONGO_DATABASE]
