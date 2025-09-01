import re

PKG = "nginx-core"
SERVICE = "nginx"


def test_package_installed(host):
    assert host.package(PKG).is_installed


def test_service_enabled_running(host):
    s = host.service(SERVICE)
    assert s.is_enabled
    assert s.is_running


def test_dirs(host):
    d = host.file("/etc/nginx/conf.d")
    assert d.exists and d.is_directory
    assert d.user == "root" and d.group == "root" and d.mode == 0o755


def test_nginx_conf_permissions(host):
    f = host.file("/etc/nginx/nginx.conf")
    assert f.exists and f.is_file
    assert f.user == "root" and f.group == "root" and f.mode == 0o644


def test_default_site_removed(host):
    assert not host.file("/etc/nginx/sites-available/default").exists
    assert not host.file("/etc/nginx/sites-enabled/default").exists


def test_site_installed_and_enabled(host):
    avail = host.file("/etc/nginx/sites-available/example.conf")
    enabled = host.file("/etc/nginx/sites-enabled/example.conf")
    assert avail.exists and avail.is_file
    assert enabled.exists and enabled.is_symlink
    assert enabled.linked_to == "/etc/nginx/sites-available/example.conf"


def test_dhparams(host):
    f = host.file("/etc/nginx/dhparams.pem")
    assert f.exists and f.is_file
    assert f.user == "root" and f.group == "root" and f.mode == 0o600


def test_hosts_deny(host):
    f = host.file("/etc/nginx/hosts.deny")
    assert f.exists and f.is_file
    assert f.user == "root" and f.group == "root" and f.mode == 0o644


def test_htpasswd_files(host):
    users = host.file("/etc/nginx/htpasswd.users")
    admins = host.file("/etc/nginx/htpasswd.admins")
    assert users.exists and users.is_file and users.user == "www-data"
    assert admins.exists and admins.is_file and admins.user == "www-data"
    assert "user1:$apr1$abcd1234$N6Hh8GmVtI8p5m2xPRw9o/" in users.content_string
    assert (
        "admin:$2y$12$B9mQXGvQe0tqJx...rest_of_bcrypt_hash..." in admins.content_string
    )


def test_http_limit_zones_conf(host):
    f = host.file("/etc/nginx/conf.d/http_limit_zones.conf")
    assert f.exists and f.is_file
    c = f.content_string
    assert re.search(
        r"geo \$limit_ip\s*{\s*default 1;\s*192\.168\.0\.0/16 0;\s*10\.0\.0\.0/8 0;",
        c,
        re.S,
    )
    assert re.search(
        r"map \$http_x_rate_limit_bypass \$limit_hdr_1\s*{\s*default \$binary_remote_addr;",
        c,
        re.S,
    )
    assert re.search(r'\n\s*secret-value\s*"";\n', c)
    assert re.search(r'\n\s*another-secret-value\s*"";\n', c)
    assert re.search(r"limit_req_zone \$limit_key zone=api_zone:10m rate=5r/s;", c)
    assert "burst=10" in c and "nodelay" in c


def test_extra_conf_rendered(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "worker_rlimit_nofile 10000;" in conf
    assert "ssl_session_cache shared:SSL:10m;" in conf
    assert "ssl_session_timeout 10m;" in conf


def test_logs_paths(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "access_log /var/log/nginx/access.log;" in conf
    assert "error_log /var/log/nginx/error.log warn;" in conf


def test_tls_core_settings(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "ssl_protocols TLSv1.2 TLSv1.3;" in conf
    assert "ssl_prefer_server_ciphers off;" in conf
    assert "ssl_ciphers HIGH:!aNULL:!MD5;" in conf
    assert "ssl_dhparam /etc/nginx/dhparams.pem;" in conf


def test_core_http_toggles(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "sendfile on;" in conf
    assert "tcp_nopush on;" in conf
    assert "tcp_nodelay on;" in conf
    assert "keepalive_timeout 75s;" in conf
    assert "keepalive_requests 1000;" in conf
    assert "server_tokens off;" in conf
    assert "include /etc/nginx/mime.types;" in conf
    assert "default_type application/octet-stream;" in conf


def test_gzip_settings(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "gzip on;" in conf
    assert "gzip_http_version 1.1;" in conf
    assert "gzip_vary off;" in conf
    assert "gzip_comp_level 3;" in conf
    assert "gzip_proxied off;" in conf
    assert "gzip_types text/css" in conf
    assert "gzip_buffers 16 8k;" in conf


def test_client_limits(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "client_max_body_size 10m;" in conf
    assert "client_body_buffer_size 16k;" in conf
    assert "large_client_header_buffers 4 8k;" in conf


def test_includes_and_sites(host):
    conf = host.file("/etc/nginx/nginx.conf").content_string
    assert "include /etc/nginx/conf.d/*.conf;" in conf
    assert "include /etc/nginx/sites-enabled/*;" in conf
    assert "include /etc/nginx/hosts.deny;" in conf


def test_systemd_override(host):
    f = host.file("/etc/systemd/system/nginx.service.d/override.conf")
    assert f.exists and f.is_file and f.user == "root" and f.group == "root"
    content = f.content_string
    assert "LimitNOFILE=10000" in content


def test_nginx_configtest(host):
    c = host.run("/usr/sbin/nginx -t")
    assert c.rc == 0
