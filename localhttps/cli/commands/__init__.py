from typing import Optional
import asyncclick as click
import os
from aiopath import AsyncPath
from localhttps.app import App
from localhttps.cli import with_context, Context
from localhttps.cmd import DefaultConsoleCmd


async def resolve_default_data_path() -> AsyncPath:
    data_path = os.environ.get('LOCALHTTPS_DATA', default=None)

    if data_path is not None:
        data_path = await AsyncPath(data_path).absolute()
    else:
        config_home = os.environ.get('XDG_CONFIG_HOME', default=None)
        if config_home is not None:
            config_home = await AsyncPath(config_home).absolute()
        else:
            config_home = await ((await AsyncPath.home())/'.config').absolute()

        data_path: AsyncPath = config_home/'localhttps'

    await data_path.mkdir(exist_ok=True)
    return data_path

@click.group()
@click.option('--data-path', default=None, help='Base data path (defaults to $LOCALHTTPS_DATA or $XDG_CONFIG_HOME/localhttps (~/.config/localhttps))')
@click.option('--verbose/-V', default=False, help='Verbose output')
@with_context
async def cli(ctx: Context, data_path: Optional[str], verbose: bool):
    if data_path is not None:
        ctx.data_path = await AsyncPath(data_path).absolute()
    else:
        ctx.data_path = await resolve_default_data_path()

    ctx.app = App(ctx.data_path)

    if verbose and isinstance(ctx.cmd, DefaultConsoleCmd):
        ctx.cmd.verbose = True

import localhttps.cli.commands.init
import localhttps.cli.commands.secure
import localhttps.cli.commands.status
import localhttps.cli.commands.unsecure
import localhttps.cli.commands.use
