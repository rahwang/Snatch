# Snatch

A web implementation of the game snatch.


## Development

You need `yarn` and `poetry` installed.

## Server

Install dependencies:

```
poetry install
```

Run server:

```
poetry run websocket-server
```

The server runs on `ws://localhost:8765` for now.


## Client

First, `cd` into the `snatch-client` directory.

Install dependencies:

```
yarn install
```

You might get an error about an incompatible version of engine node. If you do, try:

```
yarn install --ignore-engines
```

Run client:

```
yarn start
```

You should be taken to localhost:3000 in your browser, but if not you
can navigate there manually.
