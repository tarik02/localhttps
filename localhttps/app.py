from typing import Optional
from aiopath import AsyncPath

from localhttps.cert.ca import CertificationAuthority
from localhttps.cert.cert import Certificate

class App:
    _data_path: AsyncPath

    def __init__(self, data_path: AsyncPath) -> None:
        self._data_path = data_path

    def ca(self, name: str = 'default') -> CertificationAuthority:
        return CertificationAuthority(self._data_path/'CertificationAuthorities', name)

    def cert(self, name: str, domain: str, ca: Optional[CertificationAuthority] = None) -> Certificate:
        if ca is None:
            ca = self.ca()

        return Certificate(
            authority=ca,
            root_path=self._data_path/'Certificates'/ca.name,
            name=name,
            domain=domain,
        )

    async def generate_nginx_config(self, cert: Certificate, out_path: AsyncPath):
        await out_path.write_text(f'''
ssl_certificate {await cert.crt_path.resolve()};
ssl_certificate_key {await cert.key_path.resolve()};
'''.strip())

    async def generate_universal_nginx_config(self, ca: CertificationAuthority, out_path: AsyncPath):
        key_path_prefix = await (self._data_path/'Certificates'/ca.name).resolve()
        await out_path.write_text(f'''
ssl_certificate {key_path_prefix}/$ssl_server_name.crt;
ssl_certificate_key {key_path_prefix}/$ssl_server_name.key;
'''.strip())
