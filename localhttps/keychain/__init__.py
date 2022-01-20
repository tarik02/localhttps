import platform

from localhttps.keychain.linux import LinuxKeychain
from localhttps.keychain.macos import MacOSKeychain


def get_current_keychain():
    name = platform.system()

    if name == 'Linux':
        return LinuxKeychain()
    elif name == 'Darwin':
        return MacOSKeychain()
    else:
        raise ValueError(f'Platform {name} is not supported')
