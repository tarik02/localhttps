import asyncclick as click
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context


@cli.command(help='Delete certificate for domain')
@click.argument('domain')
@click.option('--nginx/--no-nginx', default=False, help='Delete nginx config')
@with_context
async def unsecure(ctx: Context, domain: str, nginx: bool):
    if not await ctx.ca.exists():
        ctx.console.print(f'[red]certification authority [blue]{ctx.ca.name}[/blue] is not created[/red]')
        ctx.exit(1)

    cert = ctx.app.cert(
        domain=domain,
        name=domain,
        ca=ctx.ca,
    )

    if not await cert.exists():
        ctx.console.print(f'[red]certificate is not created[/red]')
        ctx.exit(1)

    await cert.delete()

    if nginx:
        out_path = await (ctx.data_path/'Nginx'/'ssl'/f'{domain}.conf').resolve()
        await out_path.unlink(missing_ok=True)
