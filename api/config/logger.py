# import logging
# import sys
# from flask import Flask, request, g
# import time


# def get_logger(name: str) -> logging.Logger:
#     logger = logging.getLogger(name)
#     if not logger.handlers:
#         handler = logging.StreamHandler(sys.stdout)
#         handler.setFormatter(logging.Formatter(
#             '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
#             datefmt='%Y-%m-%dT%H:%M:%S'
#         ))
#         logger.addHandler(handler)
#         logger.setLevel(logging.INFO)

#     return logger


# def register_request_logging(app: Flask) -> None:
#     logger = get_logger('app.request')

#     @app.before_request
#     def before_request():
#         g.start_time = time.monotonic()

#     @app.after_request
#     def after_request(response):
#         duration_ms = round((time.monotonic() - g.start_time) * 1000, 2)
#         logger.info('%s %s %s %dms', request.method, request.path, response.status_code, duration_ms)
#         return response
