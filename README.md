# example-project

Simple client application using websockets, and three equivalent backend implementations:

1. [aiohttp](https://docs.aiohttp.org/en/stable)
2. [tornado](https://www.tornadoweb.org/en/stable/index.html)
3. [fastapi](https://fastapi.tiangolo.com)

## Project setup

Steps to get project up and running

### Client setup


```
npm install
npm run build
```

This will install dependencies and build the application.

### Server setup

Within the `server` directory, find three subdirectories, one for each implementation.

#### Tornado

Install:

```
python3 -m venv server/tornado/tornado_venv
source server/tornado/tornado_venv/bin/activate
pip install --upgrade pip tornado
```

Run:

```
python server/tornado/main.py
```

#### aiohttp

Install:

```
python3 -m venv server/aiohttp/aiohttp_venv
source server/aiohttp/aiohttp_venv/bin/activate
pip install --upgrade pip aiohttp[speedups]
```

Run:

```
python server/aiohttp/main.py
```

#### FastAPI

Install:

```
python3 -m venv server/fastapi/fastapi_venv
source server/fastapi/fastapi_venv/bin/activate
pip install --upgrade pip fastapi[all]
```

Run:

```
python server/fastapi/main.py
```


## Run the client application

Point your browser at http://localhost:8080/static/index.html
