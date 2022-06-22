import asyncio
import asyncclick as click
from rich.console import Console
from localhttps.app import App
from localhttps.cli.commands import cli
from localhttps.cli.context import Context
from localhttps.cmd import DefaultConsoleCmd
from localhttps.keychain import get_current_keychain

async def create_context():
    ctx = Context()
    ctx.console = Console(soft_wrap=True, stderr=True)
    ctx.cmd = DefaultConsoleCmd(ctx.console)
    ctx.keychain = get_current_keychain()
    return ctx

def main():
    ctx = asyncio.run(create_context())
    cli(_anyio_backend='asyncio', obj=ctx)
