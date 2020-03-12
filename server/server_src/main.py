import os
import sys
from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth
from server_src.resources.post import Post, PostList
from server_src.resources.source import Source, SourceList

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth()

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    postgres_host = "host.docker.internal" if "DB_HOST" not in os.environ else os.environ["DB_HOST"]
    token_path = "/resources/auth_token.txt" if "TOKEN_PATH" not in os.environ else os.environ["TOKEN_PATH"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    postgres_host = sys.argv[2]
    token_path = sys.argv[3]

else:
    ENV = "dev"
    postgres_host = "localhost"
    token_path = "../../resources/auth_token.txt"


@auth.verify_token
def verify_token(token):
    correct_token = open(token_path).readline().strip()

    if token == correct_token:
        return True

    else:
        return False


@auth.error_handler
def handle_error():
    return {"status": "401 - Unauthorized."}, 401


postApi = Post.setup(postgres_host, auth)
postListApi = PostList.setup(postgres_host, auth)

sourceApi = Source.setup(postgres_host, auth)
sourceListApi = SourceList.setup(postgres_host, auth)

api.add_resource(postApi, "/blog/posts/<int:post_id>")
api.add_resource(postListApi, "/blog/posts")
api.add_resource(sourceApi, "/blog/sources/<string:source_code>")
api.add_resource(sourceListApi, "/blog/sources")

if __name__ == "__main__":
    if ENV != "prod":
        app.run(debug=True)

    else:
        app.run(debug=False, host="0.0.0.0")
