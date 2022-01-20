# LocalHTTPS

## Installation

### From Source

### From PyPI

```
pip install localhttps
```

```
git clone https://github.com/Tarik02/localhttps
cd localhttps
pip install .
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
    - /home/<username>/.config/localhttps:/home/<username>/.config/localhttps
```
