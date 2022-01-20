from abc import ABC, abstractmethod
import asyncio
from typing import Tuple
from rich.console import Console
from rich.text import Text


class Cmd(ABC):
    @abstractmethod
    async def run(self, command, *args, **kwargs) -> asyncio.subprocess.Process:
        pass


class DefaultConsoleCmd(Cmd):
    _console: Console

    verbose = False

    def __init__(self, console: Console) -> None:
        self._console = console

    async def _capture_output(self, stream: asyncio.StreamReader, label: str) -> bytes:
        buffer = b''
        while True:
            line = await stream.readline()
            if line == b'':
                break
            buffer += line

            if self.verbose:
                if not line.endswith(b'\n'):
                    self._console.print(label, Text(line.decode('utf-8')), '%', sep='')
                else:
                    self._console.print(label, Text(line.decode('utf-8')[0:-1]), sep='')

        return buffer

    async def run(self, command, *args, **kwargs) -> Tuple[int, bytes, bytes]:
        full_command = f'{command} {" ".join(args)}'
        if self.verbose:
            self._console.print(f'$ [blue]{full_command}[/blue]')
        with self._console.status(command):
            proc = await asyncio.subprocess.create_subprocess_exec(
                command,
                *args,
                **kwargs,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr, exit_code = await asyncio.gather(
                self._capture_output(proc.stdout, label='[blue]\[stdout][/blue] '),
                self._capture_output(proc.stderr, label='[blue]\[stdout][/blue] '),
                proc.wait()
            )

            if self.verbose or exit_code != 0:
                self._console.print(f'[blue]{command}[/blue] exited with code [blue]{exit_code}[/blue]')
