from enum import Enum


class CommonEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class DatabaseServices(CommonEnum):
    MONGODB = "mongodb"
    POSTGRESDB = "postgresdb"
