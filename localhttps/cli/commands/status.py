from typing import List
import asyncclick as click
from localhttps.cert.ca import CertificationAuthority
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context


async def desync(it):
    for x in it: yield x

@cli.command(help='List CA and their certificates')
@click.argument('ca', nargs=-1)
@with_context
async def status(ctx: Context, ca: List[str]):
    if len(ca) == 0:
        authorities = ctx.app.list_ca()
    else:
        authorities = desync(ctx.app.ca(name) for name in ca)

    async for ca in authorities:
        ca: CertificationAuthority

        if await ca.exists():
            ctx.console.print(f'ca [blue]{ca.name}[/blue]:')

            async for cert in ctx.app.list_certs(ca):
                ctx.console.print(f' - [blue]{cert.name}[/blue] (https://{cert.domain})')
        else:
            ctx.console.print(f'[red]ca [blue]{ca.name}[/blue]: not created[/red]')
