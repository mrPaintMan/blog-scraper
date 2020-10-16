import os
import sys

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    resource_path = "/resources/" if "TOKEN_PATH" not in os.environ else os.environ["TOKEN_PATH"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    resource_path = sys.argv[3]

else:
    ENV = "dev"
    resource_path = ""

bind = "0.0.0.0:5000"
workers = 2

if ENV != "dev":
    keyfile = f"{resource_path}Cloudflare_Origin_CA.key"
    certfile = f"{resource_path}Cloudflare_Origin_CA.crt"

else:
    keyfile = ""
    certfile = ""
