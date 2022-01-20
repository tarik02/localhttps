# LocalHTTPS

## Installation

### From Source

```
git clone https://github.com/Tarik02/localhttps
cd localhttps
pip install .
```

### From PyPI

```
pip install localhttps
```


## Usage

### Initialize

Once execute this command:
```
$ localhttps init --trust --nginx
```

This command will generate certification authority for certificates, add it to system or browser keychain (`--trust`) and will generate universal nginx config for it (`--nginx`).


### Generate certificate

Then for every domain you use:
```
$ localhttps secure --nginx example.test
```

This command will generate certificate based on previous certification authority and generate nginx config (`--nginx`) with `ssl_certificate` and `ssl_certificate_key` directives.
