import pulumi
from mailhog import Mailhog
from mailhogConfigmap import MailhogConfigmap
from mailhogWeb import MailhogWeb
from mailhogcrapi import Mailhogcrapi

mailhog = Mailhog("mailhog")
mailhog_web = MailhogWeb("mailhogWeb")
mailhog_configmap = MailhogConfigmap("mailhogConfigmap")
mailhogcrapi = Mailhogcrapi("mailhogcrapi")
