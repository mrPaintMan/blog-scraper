# Server
The server application serves to provide the scraped data through a flask rest api.
No write endpoints exists, GET is the only allowed request method.

### Resources

- /blog/posts?page=0[&source={source_code}]
- /blog/posts/{id}
- /blog/sources
- /blog/sources/{source_code}

where:
- `source_code` is a string
- `id` is an integer

### Authorization

To be able to read data from the server, an authorization header needs to be present, containing a bearer token. 
This token is a base64 encoded image, and can be found in the resources folder.

### Installation

For installing dependencies, see [this readme](https://github.com/mrPaintMan/blog-scraper/blob/master/README.md).

to run:

```
$ docker build -t {image_name} ./server
$ docker run -d \
    -p 5000:5000 \
    -e ENV={env} \
    -e DB_HOST={db_host} \
    -v {absolute_path}:/resources \
    --name {container_name} \
    {image:tag}
```
where :
- `env` is either `dev` or `prod`
- `db_host` is just the db host such as `localhost` or `host.docker.internal`
- `absolute_path` is the absolute path to the folder containing `auth_token.txt`

