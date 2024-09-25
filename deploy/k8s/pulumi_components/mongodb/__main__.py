import pulumi
from mongodb import Mongodb
from mongodb1 import Mongodb1
from mongodbConfig import MongodbConfig
from mongodbPvClaim import MongodbPvClaim

mongodb_config = MongodbConfig("mongodbConfig")
mongodb = Mongodb("mongodb")
mongodb_pv_claim = MongodbPvClaim("mongodbPvClaim")
mongodb1 = Mongodb1("mongodb1")
