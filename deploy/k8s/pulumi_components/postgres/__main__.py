import pulumi
from postgresConfig import PostgresConfig
from postgresPvClaim import PostgresPvClaim
from postgresdb import Postgresdb
from postgresdb1 import Postgresdb1

postgres_config = PostgresConfig("postgresConfig")
postgresdb = Postgresdb("postgresdb")
postgres_pv_claim = PostgresPvClaim("postgresPvClaim")
postgresdb1 = Postgresdb1("postgresdb1")
