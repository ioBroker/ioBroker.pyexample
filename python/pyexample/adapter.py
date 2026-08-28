"""A complete, if small, ioBroker adapter written in Python.

It stands in for a real device driver: it publishes a reading, accepts a
switch command and answers messages. Everything a production adapter needs is
present, only the device behind it is simulated.

Configuration comes from the instance object's ``native`` section, which the
admin UI edits through ``admin/jsonConfig.json`` -- exactly as for a Node
adapter.
"""

from __future__ import annotations

import asyncio
import math
import time

from iobroker import Adapter, Message, State


class PyExampleAdapter(Adapter):
    async def on_ready(self) -> None:
        # native comes from the instance object; the defaults keep the adapter
        # working even when it has never been configured.
        self.interval = float(self.config.get("interval") or 3)
        self.amplitude = float(self.config.get("amplitude") or 2)

        await self.set_object_not_exists(
            "temperature",
            {
                "type": "state",
                "common": {
                    "name": "Temperature",
                    "type": "number",
                    "role": "value.temperature",
                    "unit": "°C",
                    "read": True,
                    "write": False,
                },
            },
        )
        await self.set_object_not_exists(
            "switch",
            {
                "type": "state",
                "common": {
                    "name": "Switch",
                    "type": "boolean",
                    "role": "switch",
                    "read": True,
                    "write": True,
                },
            },
        )

        # Only our own states -- anything else would be noise.
        await self.subscribe_states("*")
        await self.set_state("info.connection", True, ack=True)

        self._worker = asyncio.create_task(self._measure())
        self.log.info(
            f"Publishing every {self.interval}s with amplitude {self.amplitude}"
        )

    async def _measure(self) -> None:
        """Stands in for a real measurement source."""
        try:
            while True:
                value = round(20 + self.amplitude * math.sin(time.time() / 10), 2)
                # ack=True: a confirmed reading, not a command.
                await self.set_state("temperature", value, ack=True)
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            raise

    async def on_state_change(self, id: str, state: State | None) -> None:
        if state is None:
            self.log.debug(f"{id} deleted or expired")
            return
        # ack=False means somebody wants something switched. Confirming with
        # ack=True is what stops the command from bouncing back at us.
        if not state.ack and id.endswith(".switch"):
            self.log.info(f"Switch command: {state.val}")
            await self.set_state("switch", state.val, ack=True)

    async def on_message(self, msg: Message) -> None:
        if msg.command == "ping":
            await self.reply(msg, {"pong": True})
        else:
            self.log.debug(f"Unhandled command '{msg.command}' from {msg.from_}")

    async def on_unload(self) -> None:
        worker = getattr(self, "_worker", None)
        if worker:
            worker.cancel()
        self.log.info("Stopped")
