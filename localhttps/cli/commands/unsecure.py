from typing import List
import asyncclick as click
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context
from localhttps.utils.domain import normalize_domain


@cli.command(help='Delete certificate for domain')
@click.option('--ca', default='default', help='Certification authority name')
@click.argument('domain', nargs=-1)
@with_context
async def unsecure(ctx: Context, ca: str, domain: List[str]):
    ca = ctx.app.ca(ca)
    domains = domain

    if not await ca.exists():
        ctx.console.print(f'[red]certification authority [blue]{ca.name}[/blue] is not created[/red]')
        ctx.exit(1)

    for domain in domains:
        domain = normalize_domain(domain)

        cert = ctx.app.cert(
            domain=domain,
            name=domain,
            ca=ca,
        )

        if not await cert.exists():
            ctx.console.print(f'[red]certificate [blue]{domain}[/blue] not found[/red]')
            ctx.exit(1)

        await cert.delete()

        ctx.console.print(f'certificate [blue]{domain}[/blue] removed')

        nginx_path = await (ctx.data_path/'Nginx'/'ssl'/f'{domain}.conf').absolute()
        if await nginx_path.exists():
            await nginx_path.unlink(missing_ok=True)
            ctx.console.print(f'deleted [blue]{nginx_path}[/blue]')
