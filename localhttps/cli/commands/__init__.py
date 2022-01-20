import asyncclick as click
from localhttps.cli import with_context, Context
from localhttps.cmd import DefaultConsoleCmd


@click.group()
@click.option('--ca', default='default', help='Certification authority name')
@click.option('--verbose/-V', default=False, help='Verbose output')
@with_context
async def cli(ctx: Context, ca: str, verbose: bool):
    ctx.ca = ctx.app.ca(ca)
    if verbose and isinstance(ctx.cmd, DefaultConsoleCmd):
        ctx.cmd.verbose = True

import localhttps.cli.commands.init
import localhttps.cli.commands.secure
import localhttps.cli.commands.unsecure
