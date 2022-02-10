import asyncio
from typing import List, Tuple
from aiopath import AsyncPath

from localhttps.cmd import Cmd

class CertificationAuthority:
    _root_path: AsyncPath
    _name: str

    def __init__(self, root_path: AsyncPath, name: str) -> None:
        self._root_path = root_path
        self._name = name

    @property
    def path(self) -> AsyncPath:
        return self._root_path

    @property
    def name(self) -> str:
        return self._name

    @property
    def key_path(self) -> AsyncPath:
        return self._root_path/f'{self._name}.key'

    @property
    def pem_path(self) -> AsyncPath:
        return self._root_path/f'{self._name}.pem'

    @property
    def srl_path(self) -> AsyncPath:
        return self._root_path/f'{self._name}.srl'

    @property
    def org_name(self) -> str:
        return 'LocalHTTPS CA Self Signed Organization'

    @property
    def common_name(self) -> str:
        return 'LocalHTTPS CA Self Signed CN'

    @property
    def email(self) -> str:
        return f'{self._name}@localhttps'

    @property
    def subject_parts(self) -> List[Tuple[str, str]]:
        return [
            ('C', ''),
            ('ST', ''),
            ('O', self.org_name),
            ('localityName', ''),
            ('commonName', self.common_name),
            ('organizationalUnitName', 'Developers'),
            ('emailAddress', self.email),
        ]

    @property
    def subject(self) -> str:
        return ''.join(
            f'/{key}={value}' for (key, value) in self.subject_parts
        ) + '/'

    async def exists(self) -> bool:
        key_exists, pem_exists = await asyncio.gather(self.key_path.exists(), self.pem_path.exists())
        return key_exists and pem_exists

    async def create(self, cmd: Cmd) -> None:
        await self.delete()
        await self._root_path.mkdir(parents=True, exist_ok=True)

        await cmd.run(
            'openssl',
            'req',
            '-new',
            '-newkey', 'rsa:2048',
            '-days', '730',
            '-nodes',
            '-x509',
            '-subj',
            self.subject,
            '-keyout', str(await self.key_path.absolute()),
            '-out', str(await self.pem_path.absolute()),
        )

    async def delete(self) -> None:
        await asyncio.gather(
            self.key_path.unlink(missing_ok=True),
            self.pem_path.unlink(missing_ok=True),
        )
        if await self._root_path.exists():
            async for _ in self._root_path.glob('*'):
                return
            self._root_path.rmdir()
