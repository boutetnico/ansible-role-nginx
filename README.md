[![tests](https://github.com/boutetnico/ansible-role-nginx/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-nginx/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.nginx-blue.svg)](https://galaxy.ansible.com/boutetnico/nginx)

ansible-role-nginx
==================

This role installs [Nginx](https://nginx.org/index.html).

Requirements
------------

Ansible 2.10 or newer.

Supported Platforms
-------------------

- [Debian - 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                             | Required | Default                       | Choices     | Comments                            |
|--------------------------------------|----------|-------------------------------|-------------|-------------------------------------|
| `nginx_packages`                     | true     | `["nginx-core"]`              | list(str)   | Packages to install                 |
| `nginx_user`                         | true     | `"www-data"`                  | string      | Nginx user                          |
| `nginx_mime_file_path`               | true     | `"/etc/nginx/mime.types"`     | string      | MIME types file                     |
| `nginx_pidfile`                      | true     | `"/run/nginx.pid"`            | string      | PID file                            |
| `nginx_access_log`                   | true     | `"/var/log/nginx/access.log"` | string      | Access log path                     |
| `nginx_error_log`                    | true     | `"/var/log/nginx/error.log"`  | string      | Error log path                      |
| `nginx_multi_accept`                 | true     | `false`                       | bool        |                                     |
| `nginx_worker_connections`           | true     | `512`                         | int         |                                     |
| `nginx_worker_processes`             | true     | `"auto"`                      | string/int  | Master process count                |
| `nginx_default_type`                 | true     | `"application/octet-stream"`  | string      |                                     |
| `nginx_keepalive_requests`           | true     | `1000`                        | int         |                                     |
| `nginx_keepalive_timeout`            | true     | `"75s"`                       | string      |                                     |
| `nginx_sendfile`                     | true     | `true`                        | bool        |                                     |
| `nginx_server_name_in_redirect`      | true     | `false`                       | bool        |                                     |
| `nginx_server_names_hash_bucket_size`| true     | `64`                          | int         |                                     |
| `nginx_server_names_hash_max_size`   | true     | `512`                         | int         |                                     |
| `nginx_server_tokens`                | true     | `false`                       | bool        |                                     |
| `nginx_tcp_nodelay`                  | true     | `true`                        | bool        |                                     |
| `nginx_tcp_nopush`                   | true     | `true`                        | bool        |                                     |
| `nginx_types_hash_max_size`          | true     | `2048`                        | int         |                                     |
| `nginx_gzip`                         | true     | `true`                        | bool        |                                     |
| `nginx_gzip_buffers`                 | true     | `"16 8k"`                     | string      |                                     |
| `nginx_gzip_comp_level`              | true     | `3`                           | int         |                                     |
| `nginx_gzip_http_version`            | true     | `"1.1"`                       | string      |                                     |
| `nginx_gzip_proxied`                 | true     | `"off"`                       | string      |                                     |
| `nginx_gzip_types`                   | true     |                               | string      | See `defaults/main.yml`             |
| `nginx_gzip_vary`                    | true     | `false`                       | bool        |                                     |
| `nginx_dhparams_path`                | true     | `"/etc/nginx/dhparams.pem"`   | string      | Used by `ssl_dhparam`               |
| `nginx_dhparams_size`                | true     | `2048`                        | int         | Generated if missing                |
| `nginx_ssl_ciphers`                  | true     | `"HIGH:!aNULL:!MD5"`          | string      | TLS cipher string                   |
| `nginx_ssl_prefer_server_ciphers`    | true     | `false`                       | bool        |                                     |
| `nginx_ssl_protocols`                | true     | `"TLSv1.2 TLSv1.3"`           | string      | Enabled protocols                   |
| `nginx_client_body_buffer_size`      | true     | `"16k"`                       | string      |                                     |
| `nginx_client_max_body_size`         | true     | `"10m"`                       | string      |                                     |
| `nginx_large_client_header_buffers`  | true     | `"4 8k"`                      | string      |                                     |
| `nginx_deny_hosts_file`              | true     | `"/etc/nginx/hosts.deny"`     | string      | Included in http {}                 |
| `nginx_http_limit_whitelist_cidrs`   | true     | `[]`                          | list(str)   | CIDRs whitelisted                   |
| `nginx_http_limit_whitelist_headers` | true     | `[]`                          | list(dict)  | See `defaults/main.yml`             |
| `nginx_http_limit_zones`             | true     | `[]`                          | list(dict)  | See `defaults/main.yml`             |
| `nginx_servers`                      | true     | `[]`                          | list(dict)  | See `defaults/main.yml`             |
| `nginx_auth`                         | true     | `[]`                          | list(dict)  | See `defaults/main.yml`             |
| `nginx_extra_conf_root`              | true     | `{}`                          | dict        | Extra root-level directives         |
| `nginx_extra_conf_http`              | true     | `{}`                          | dict        | Extra http-level directives         |
| `nginx_systemd_override`             | true     | `{}`                          | dict        | See `defaults/main.yml`             |

Dependencies
------------

None

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-nginx

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
