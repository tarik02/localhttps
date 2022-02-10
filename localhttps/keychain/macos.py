from typing import AsyncIterable, List

from localhttps.cert.ca import CertificationAuthority
from localhttps.keychain.abc import AbstractKeychain
from localhttps.cmd import Cmd
from localhttps.utils.cli import ask_to_run_command


class MacOSKeychain(AbstractKeychain):
    async def databases(self) -> AsyncIterable[str]:
        yield '/Library/Keychains/System.keychain'

    async def trust_ca(self, cmd: Cmd, ca: CertificationAuthority, database: str):
        await ask_to_run_command(f'sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "{await ca.pem_path.absolute()}"')
