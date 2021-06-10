# Websocket Server Experimentation

Simple client application using websockets, and three equivalent backend implementations:

1. [aiohttp](https://docs.aiohttp.org/en/stable)
2. [tornado](https://www.tornadoweb.org/en/stable/index.html)
3. [fastapi](https://fastapi.tiangolo.com)

## Project setup

Steps to get project up and running.  All commands given below should be executed from the root of the repo.  At a high level the steps are:

1. Build the client application (Client setup)
2. Install and run a server implementation (Pick one from Server setup)
3. Run the application (point your browser at http://localhost:8080/static/index.html)

### Client setup

```
npm install
npm run build
```

This will install dependencies and build the application.

### Server setup

Within the `server` directory, you should find three subdirectories, one for each implementation.

#### Tornado

Install:

```
python3 -m venv server/tornado/tornado_venv
source server/tornado/tornado_venv/bin/activate
pip install --upgrade pip
pip install tornado
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
pip install --upgrade pip
pip install aiohttp[speedups]
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
pip install --upgrade pip
pip install fastapi[all]
```

Run:

```
python server/fastapi/main.py
```
