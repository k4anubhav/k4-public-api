import math
import multiprocessing
import os

# bind = "unix:/run/wyse_gunicorn.sock"
bind = "0.0.0.0:8080"

# Logging documentation: http://docs.gunicorn.org/en/stable/settings.html#accesslog
# using X-Forwarded-For header for the request source ip as host ip
# at gunicorn will be the local nginx ip i.e 127.0.0.1
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s"'

# redirect to stdout
from pathlib import Path

proj_path = Path(__file__).resolve().parent

# accesslog = f"{proj_path}/logs/gunicorn/access.log"
# errorlog = f"{proj_path}/logs/gunicorn/error.log"
accesslog = "-"  # goes to stderr (i.e. nowhere)
errorlog = "-"
loglevel = "DEBUG"
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# http://docs.gunicorn.org/en/stable/settings.html#limit-request-line
# requests from homebase exceed an url length of 8190,
# and since a url length limit is already present in nginx, this can't be abused
limit_request_line = 0

cpu_count = multiprocessing.cpu_count()


def get_cpu_quota_within_docker():
    cpu_cores = None

    cfs_period = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
    cfs_quota = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")

    if cfs_period.exists() and cfs_quota.exists():
        # we are in a linux container with cpu quotas!
        with cfs_period.open('rb') as p, cfs_quota.open('rb') as q:
            p, q = int(p.read()), int(q.read())

            # get the cores allocated by dividing the quota
            # in microseconds by the period in microseconds
            cpu_cores = q / p if q > 0 and p > 0 else None

    return cpu_cores


# cpu_cores = get_cpu_quota_within_docker() or multiprocessing.cpu_count()
cpu_cores = 1
nworkers = math.floor(cpu_cores * 2 + 1)
workers = nworkers
threads = 2
graceful_timeout = 30
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "gthread")
max_requests = 50000
max_requests_jitter = 10000