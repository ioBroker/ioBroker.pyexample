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

- `io-package.json` carries `"runtime": "python"`. That is the marker
  [py-controller](https://github.com/ioBroker/ioBroker.py-controller) looks for
  when deciding what needs a virtual environment, and the one js-controller will
  eventually use to decide how to start it.
- `python/pyproject.toml` declares the dependencies. py-controller creates a
  venv from it under `iobroker-data/py/pyexample/`, isolated from every other
  adapter.

Everything else is an ordinary ioBroker adapter: npm package, `io-package.json`,
`admin/jsonConfig.json`. That keeps the repository, the repo checker,
`iobroker add`, admin updates and backups working unchanged.

## Current limitation

`common.mode` is `none`, so js-controller does not start this adapter yet — the
branch that spawns an interpreter from the venv instead of `node` is not in the
core yet. Until then it runs manually:

```bash
IOB_CONFIG=/opt/iobroker/iobroker-data/iobroker.json \
  iobroker-data/py/pyexample/venv/bin/python -m pyexample --instance 0
```

Stopping already works the way the controller does it — set the `sigKill` state
to `-1` and the adapter shuts down in an orderly fashion.

## Related

- [iobroker-python](https://github.com/ioBroker/iobroker-python) — the SDK
- [ioBroker.py-controller](https://github.com/ioBroker/ioBroker.py-controller) — environment management

## License

MIT
