# LocalHTTPS

## Installation

### Option 1. Docker Image (recommended)

Add this to your aliases:
```
alias localhttps="docker run \
  -u "$(id -u "${USER}"):$(id -g "${USER}")" \
  -e "USER=${USER}" \
  -e "HOME=${HOME}" \
  -v "$HOME/.config/localhttps:$HOME/.config/localhttps" \
  -t tarik02/localhttps"
```

### Option 2. From PyPI

```
pip install localhttps
```

### Option 3. From Source

```
git clone https://github.com/Tarik02/localhttps
cd localhttps
pip install .
```

### Recommended dependencies

It's recommended to install `p11-kit` package where it's available (on Linux systems). It is used to install certification authority to system keychain.

## Usage

### Initialize

Once execute this command:
```
$ localhttps init --trust --nginx
```

This command will generate certification authority for certificates, add it to system or browser keychain (`--trust`) and will generate universal nginx config for it (`--nginx`).


### Status

```
$ localhttps status
```

Will show you list of generated certificates and domains.


### Create and use certificate for specific task

```
$ localhttps use json localhost
# {"domain":"localhost","cert":{"key":"/path/to/config/Certificates/default/localhost.key","crt":"/path/to/config/Certificates/default/localhost.crt"},"ca":{"key":"/path/to/config/CertificationAuthorities/default.key","pem":"/path/to/config/CertificationAuthorities/default.pem"}}

$ localhttps use webpack localhost
# --client-web-socket-url-hostname='localhost' --server-type https --server-options-key='/path/to/config/Certificates/default/localhost.key' --server-options-cert='/path/to/config/Certificates/default/localhost.crt' --server-options-ca='/path/to/config/CertificationAuthorities/default.pem'

$ localhttps use -- '--key {cert[key]} --crt {cert[crt]}' localhost
# --key /home/tarik02/.config/localhttps/Certificates/default/localhost.key --crt /home/tarik02/.config/localhttps/Certificates/default/localhost.crt

# Available variable placeholders:
# {domain}
# {cert[key]}
# {cert[crt]}
# {ca[key]}
# {ca[pem]}
```


### Generate certificate

Then for every domain you use:
```
$ localhttps secure --nginx example.test
```

This command will generate certificate based on previous certification authority and generate nginx config (`--nginx`) with `ssl_certificate` and `ssl_certificate_key` directives.

### nginx

If you use previous commands with `--nginx` flags, it will generate config files that can be included in server section. You just need to patch your nginx config a bit:
```
+ server {
+    listen 80;
+    server_name example.test;
+    return 301 https://$host$request_uri;
+}

server {
- listen 80;
+ listen 443 ssl;
+ include /home/<username>/.config/localhttps/Nginx/ssl/default.conf;
+ # or include /home/<username>/.config/localhttps/Nginx/ssl/example.test.conf;
```

### docker(-compose)

If you are using nginx inside docker, just map local paths to container like this:
```
services:
  nginx:
    volumes:
    - ${HOME}/.config/localhttps:${HOME}/.config/localhttps
```
