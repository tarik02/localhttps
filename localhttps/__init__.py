import asyncio
import asyncclick as click
from aiopath import AsyncPath
from rich.console import Console
from localhttps.app import App
from localhttps.cli.commands import cli
from localhttps.cli.context import Context
from localhttps.cmd import DefaultConsoleCmd
from localhttps.keychain import get_current_keychain

async def create_context():
    ctx = Context()
    ctx.console = Console(soft_wrap=True)
    ctx.cmd = DefaultConsoleCmd(ctx.console)
    ctx.data_path = (await AsyncPath.home())/'.config'/'localhttps'
    app = App(ctx.data_path)
    ctx.app = app
    ctx.keychain = get_current_keychain()
    return ctx

def main():
    ctx = asyncio.run(create_context())
    cli(_anyio_backend='asyncio', obj=ctx)
