bind = "unix:/run/gunicorn/socket"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

errorlog = "-"  # stderr
accesslog = "-"  # stdout
loglevel = "info"

worker_tmp_dir = "/dev/shm"

umask = 0o007