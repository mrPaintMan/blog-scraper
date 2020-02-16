import os
import sys
from flask import Flask
from flask_restful import Api
from server.server_src.resources.post import Post, PostList
from server.server_src.resources.source import Source, SourceList

app = Flask(__name__)
api = Api(app)

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    postgres_host = "host.docker.internal" if "DB_HOST" not in os.environ else os.environ["DB_HOST"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    postgres_host = sys.argv[2]

else:
    ENV = "dev"
    postgres_host = "localhost"

postApi = Post.setup(postgres_host)
postListApi = PostList.setup(postgres_host)

sourceApi = Source.setup(postgres_host)
sourceListApi = SourceList.setup(postgres_host)

api.add_resource(postApi, "/blog/posts/<int:post_id>")
api.add_resource(postListApi, "/blog/posts")
api.add_resource(sourceApi, "/blog/sources/<string:source_code>")
api.add_resource(sourceListApi, "/blog/sources")


if __name__ == "__main__":
    if ENV != "prod":
        app.run(debug=True)

    else:
        app.run(debug=False)
