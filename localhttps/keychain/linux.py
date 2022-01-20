from typing import AsyncIterable, List
from aiopath import AsyncPath

from localhttps.cert.ca import CertificationAuthority
from localhttps.keychain.abc import AbstractKeychain
from localhttps.cmd import Cmd


class LinuxKeychain(AbstractKeychain):
    async def databases(self) -> AsyncIterable[str]:
        p = (await AsyncPath.home())/'.pki'/'nssdb'
        if await p.exists():
            yield f'sql:{await p.resolve()}'

        async for p in ((await AsyncPath.home())/'.mozilla'/'firefox').glob('*.default'):
            yield str(await p.resolve())

    async def trust_ca(self, cmd: Cmd, ca: CertificationAuthority, database: str):
        await cmd.run(
            'certutil',
            '-d', database,
            '-A',
            '-t', 'TC',
            '-n', 'localhttps',
            '-i', str(await ca.pem_path.resolve()),
        )
