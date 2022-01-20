import rich
from typing import AsyncIterable, List

from localhttps.cert.ca import CertificationAuthority
from localhttps.keychain.abc import AbstractKeychain
from localhttps.cmd import Cmd


class MacOSKeychain(AbstractKeychain):
    async def databases(self) -> AsyncIterable[str]:
        yield '/Library/Keychains/System.keychain'

    async def trust_ca(self, cmd: Cmd, ca: CertificationAuthority, database: str):
        console = rich.get_console()
        console.print('')
        console.print('Execute the following command in terminal and press enter:')
        console.print('')
        console.print(f'    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "{await ca.pem_path.resolve()}"')
        console.print('')
        console.input('[Press enter]')
