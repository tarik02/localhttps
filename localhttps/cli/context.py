from typing import NoReturn
import asyncclick as click
from aiopath import AsyncPath
from rich.console import Console

from localhttps.app import App
from localhttps.cmd import Cmd
from localhttps.keychain.abc import AbstractKeychain


class Context:
    click: click.core.Context
    cmd: Cmd
    console: Console
    data_path: AsyncPath
    app: App
    keychain: AbstractKeychain

    def exit(self, code: int = 0) -> NoReturn:
        self.click.exit(code)
