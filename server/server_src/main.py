import os
import sys
from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth

from server_src.resources.ci import Ci
from server_src.resources.post import Post, PostList
from server_src.resources.source import Source, SourceList
from server_src.resources.register import Register
from server_src.resources.notifications import Notifications

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth()

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    host = "host.docker.internal" if "HOST" not in os.environ else os.environ["HOST"]
    resource_path = "../../resources/" if "RESOURCE_PATH" not in os.environ else os.environ["RESOURCE_PATH"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    host = sys.argv[2]
    resource_path = sys.argv[3]

else:
    ENV = "dev"
    host = "localhost"
    resource_path = "../../resources/"


@auth.verify_token
def verify_token(token):
    correct_token = open(resource_path + "auth_token.txt").readline().strip()

    if token == correct_token:
        return True

    else:
        return False


@auth.error_handler
def handle_error():
    return {"status": "401 - Unauthorized."}, 401


postApi = Post.setup(host, auth)
postListApi = PostList.setup(host, auth)

sourceApi = Source.setup(host, auth)
sourceListApi = SourceList.setup(host, auth)

registrationApi = Register.setup(host, auth)
notificationsApi = Notifications.setup(host, resource_path)

# Blog resources
api.add_resource(postApi, "/blog/posts/<int:post_id>", methods=["GET"])
api.add_resource(postListApi, "/blog/posts", methods=["GET"])
api.add_resource(sourceApi, "/blog/sources/<string:source_code>", methods=["GET"])
api.add_resource(sourceListApi, "/blog/sources", methods=["GET"])
api.add_resource(registrationApi, "/blog/register", methods=["POST"])
api.add_resource(notificationsApi, "/blog/notifications", methods=["GET"])

# Misc resources
api.add_resource(Ci, "/ci", methods=["POST"])

if __name__ == "__main__":
    if ENV != "prod":
        app.run(debug=True, host="0.0.0.0")

    else:
        context = (resource_path + "Cloudflare_Origin_CA.crt", resource_path + "Cloudflare_Origin_CA.key")
        app.run(debug=False, host="0.0.0.0", ssl_context=context)
