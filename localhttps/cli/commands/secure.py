import asyncclick as click
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context


@cli.command(help='Create certificate for domain')
@click.argument('domain')
@click.option('--force/--no-force', default=False, help='Force recreate')
@click.option('--nginx/--no-nginx', default=False, help='Generate config for nginx')
@with_context
async def secure(ctx: Context, domain: str, force: bool, nginx: bool):
    if not await ctx.ca.exists():
        ctx.console.print(f'[red]certification authority [blue]{ctx.ca.name}[/blue] is not created, use init command to create first[/red]')
        ctx.exit(1)

    cert = ctx.app.cert(
        domain=domain,
        name=domain,
        ca=ctx.ca,
    )

    if force or not await cert.exists():
        ctx.console.print('creating certificate...')
        await cert.create(ctx.cmd)
        ctx.console.print('certificate created!')
    else:
        ctx.console.print('certificate already exists, use [blue]--force[/blue] to recreate')

    if nginx:
        out_path = await (ctx.data_path/'Nginx'/'ssl'/f'{domain}.conf').absolute()
        await out_path.parent.mkdir(parents=True, exist_ok=True)
        await ctx.app.generate_nginx_config(cert, out_path)
        ctx.console.print(f'nginx config generated to {out_path}')
