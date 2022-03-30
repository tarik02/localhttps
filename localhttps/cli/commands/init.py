import asyncclick as click
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context


@cli.command(help='Initialize certification authority')
@click.option('--force-ca/--no-force-ca', default=False, help='Force create certification authority')
@click.option('--trust/--no-trust', default=False, help='Add certification authority to system keychain/browser keychains')
@click.option('--nginx/--no-nginx', default=False, help='Generate config for nginx')
@click.option('--ca', default='default', help='Certification authority name')
@with_context
async def init(ctx: Context, force_ca: bool, trust: bool, nginx: bool, ca: str):
    ca = ctx.app.ca(ca)

    if not force_ca:
        ctx.console.print('checking...')
    if force_ca or not await ca.exists():
        ctx.console.print('creating...')
        await ca.create(ctx.cmd)
        ctx.console.print('created!')
    else:
        ctx.console.print('already exists')

    ctx.console.print(f'located in {await ca.path.absolute()} with name {ca.name}')

    if trust:
        async for db in ctx.keychain.databases():
            ctx.console.print(f'adding to [blue]{db}[/blue]')
            await ctx.keychain.trust_ca(ctx.cmd, ca, database=db)

    if nginx:
        out_path = await (ctx.data_path/'Nginx'/'ssl'/f'{ca.name}.conf').absolute()
        await out_path.parent.mkdir(parents=True, exist_ok=True)
        await ctx.app.generate_universal_nginx_config(ca, out_path)
        ctx.console.print(f'nginx config generated to {out_path}')
