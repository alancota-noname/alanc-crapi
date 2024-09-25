import pulumi
from waitforGrant import WaitforGrant
from waitforReader import WaitforReader

waitfor_reader = WaitforReader("waitforReader")
waitfor_grant = WaitforGrant("waitforGrant")
