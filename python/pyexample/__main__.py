"""Entry point of the pyexample adapter.

js-controller starts a Python adapter the same way it starts a Node adapter,
passing ``--instance`` and ``--loglevel``. The SDK reads both, so there is
nothing to wire up here.
"""

from .adapter import PyExampleAdapter


def main() -> None:
    PyExampleAdapter("pyexample").run()


if __name__ == "__main__":
    main()
