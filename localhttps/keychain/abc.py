from abc import ABC, abstractmethod
from typing import AsyncIterable
from localhttps.cert.ca import CertificationAuthority

from localhttps.cmd import Cmd


class AbstractKeychain(ABC):
    @abstractmethod
    async def databases(self) -> AsyncIterable[str]:
        pass

    @abstractmethod
    async def trust_ca(self, cmd: Cmd, ca: CertificationAuthority, database: str):
        pass
