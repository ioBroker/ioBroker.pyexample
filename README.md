# ioBroker.pyexample

Example ioBroker adapter written in Python. It exists to exercise the whole
chain — SDK, packaging, environment build — with something small enough to read
in one sitting.

> **Status: 0.0.1, example.** Not meant for production use.

## What it does

Publishes a simulated temperature reading, accepts a switch command and answers
a `ping` message. Interval and amplitude are configured through the admin UI,
exactly as for a Node adapter.

## What makes it a Python adapter

Two things, and nothing else:

- `io-package.json` sets `"platform": "Python"` instead of the usual
  `Javascript/Node.js`. `platform` has always been the field describing what an
  adapter is written in; it is what
  [py-controller](https://github.com/ioBroker/ioBroker.py-controller) looks for
  when deciding what needs a virtual environment, and what js-controller uses to
  decide how to start it.
- `python/pyproject.toml` declares the dependencies. py-controller creates a
  venv from it under `iobroker-data/py/pyexample/`, isolated from every other
  adapter.

Everything else is an ordinary ioBroker adapter: npm package, `io-package.json`,
`admin/jsonConfig.json`. That keeps the repository, the repo checker,
`iobroker add`, admin updates and backups working unchanged.

## Running it

js-controller starts, supervises and stops this adapter like any other, so
`iobroker start pyexample.0` and `iobroker stop pyexample.0` work as usual. That
needs a js-controller which understands `platform: "Python"`; until that support
is released, the adapter can be started by hand from its environment:

```bash
IOB_CONFIG=/opt/iobroker/iobroker-data/iobroker.json   iobroker-data/py/pyexample/venv/bin/python -m pyexample --instance 0
```

## Related

- [iobroker-python](https://github.com/ioBroker/iobroker-python) — the SDK
- [ioBroker.py-controller](https://github.com/ioBroker/ioBroker.py-controller) — environment management

## License

MIT
