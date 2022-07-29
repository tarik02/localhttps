from typing import List
import asyncclick as click
import json
from localhttps.cli import with_context
from localhttps.cli.commands import cli
from localhttps.cli.context import Context
from localhttps.utils.domain import normalize_domain

DEFAULT_FORMATS = {
    'webpack': "'--client-web-socket-url-hostname={domain}' --server-type https '--server-options-key={cert[key]}' '--server-options-cert={cert[crt]}' '--server-options-ca={ca[pem]}'",
}

@cli.command(help='Create certificate and print it with given format')
@click.option('--ca', default='default', help='Certification authority name')
@click.option('--force/--no-force', default=False, help='Force recreate')
@click.argument('format')
@click.argument('domain', nargs=-1)
@with_context
async def use(ctx: Context, ca: str, force: bool, format: str, domain: List[str]):
    ca = ctx.app.ca(ca)
    domains = domain

    if not await ca.exists():
        ctx.console.print(f'[red]certification authority [blue]{ca.name}[/blue] is not created, use init command to create first[/red]')
        ctx.exit(1)

    is_first = True
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
            ctx.console.print(f'certificate [blue]{domain}[/blue] created!')

        if format in DEFAULT_FORMATS:
            format = DEFAULT_FORMATS[format]

        if is_first:
            is_first = False
        else:
            print()

        if format == 'json':
            print(
                json.dumps({
                    'domain': cert.domain,

                    'cert': {
                        'key': str(await cert.key_path.absolute()),
                        'crt': str(await cert.crt_path.absolute()),
                    },
                    'ca': {
                        'key': str(await ca.key_path.absolute()),
                        'pem': str(await ca.pem_path.absolute()),
                    },
                }, separators=(',', ':')),
                end='',
            )
        else:
            print(
                format.format(
                    domain=cert.domain,

                    cert={
                        'key': str(await cert.key_path.absolute()),
                        'crt': str(await cert.crt_path.absolute()),
                    },

                    ca = {
                        'key': str(await ca.key_path.absolute()),
                        'pem': str(await ca.pem_path.absolute()),
                    },
                ),
                end='',
            )
