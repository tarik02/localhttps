from typing import List
import asyncclick as click
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context
from localhttps.utils.domain import normalize_domain


@cli.command(help='Create certificate for domain')
@click.option('--ca', default='default', help='Certification authority name')
@click.option('--force/--no-force', default=False, help='Force recreate')
@click.option('--nginx/--no-nginx', default=False, help='Generate config for nginx')
@click.argument('domain', nargs=-1)
@with_context
async def secure(ctx: Context, ca: str, force: bool, nginx: bool, domain: List[str]):
    ca = ctx.app.ca(ca)
    domains = domain

    if not await ca.exists():
        ctx.console.print(f'[red]certification authority [blue]{ca.name}[/blue] is not created, use init command to create first[/red]')
        ctx.exit(1)

    for domain in domains:
        domain = normalize_domain(domain)

        cert = ctx.app.cert(
            domain=domain,
            name=domain,
            ca=ca,
        )

        if force or not await cert.exists():
            ctx.console.print(f'creating certificate [blue]{domain}[/blue]...')
            await cert.create(ctx.cmd)
            ctx.console.print('certificate created!')
        else:
            ctx.console.print('certificate already exists, use [blue]--force[/blue] to recreate')

        if nginx:
            out_path = await (ctx.data_path/'Nginx'/'ssl'/f'{domain}.conf').absolute()
            await out_path.parent.mkdir(parents=True, exist_ok=True)
            await ctx.app.generate_nginx_config(cert, out_path)
            ctx.console.print(f'nginx config generated to {out_path}')
