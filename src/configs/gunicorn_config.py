import multiprocessing
import os

bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '5050')}"

workers = multiprocessing.cpu_count() * 2 + 1

threads = 2

timeout = 120

graceful_timeout = 30

accesslog = "-"
errorlog = "-"
loglevel = "info"

proc_name = "boilerplate-server"
