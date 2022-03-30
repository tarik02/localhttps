from typing import AsyncIterable
from aiopath import AsyncPath
from aiofiles.os import wrap
import shutil
import rich

from localhttps.cert.ca import CertificationAuthority
from localhttps.keychain.abc import AbstractKeychain
from localhttps.cmd import Cmd
from localhttps.utils.cli import ask_to_run_command


which = wrap(shutil.which)

class LinuxKeychain(AbstractKeychain):
    async def databases(self) -> AsyncIterable[str]:
        p = (await AsyncPath.home())/'.pki'/'nssdb'
        if await p.exists():
            yield f'sql:{await p.absolute()}'

        async for p in ((await AsyncPath.home())/'.mozilla'/'firefox').glob('*.default'):
            yield str(await p.absolute())

        yield f'p11-kit'

    async def trust_ca(self, cmd: Cmd, ca: CertificationAuthority, database: str):
        console = rich.get_console()

        if database == 'p11-kit':
            trust_path = await which('trust')
            if trust_path is None:
                console.print()
                console.print('Install p11-kit and then:')

            await ask_to_run_command(f'sudo trust anchor --store {await ca.pem_path.absolute()}')
            return

        await cmd.run(
            'certutil',
            '-d', database,
            '-A',
            '-t', 'TC',
            '-n', 'localhttps',
            '-i', str(await ca.pem_path.absolute()),
        )
