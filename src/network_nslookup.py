

from dataclasses import dataclass
import time


import socket
# import urllib.request
import re


from .common_types import CheckResult

@dataclass(kw_only=True)
class NSLookupResult(CheckResult):
    pass

def get_status(target):
    success = False
    response_body = None
    error_msg = None
    duration = None
    try:
        time_start = time.perf_counter()
        response_body = socket.gethostbyname(target)
        time_end = time.perf_counter()
        duration = (time_end - time_start) * 1
        success = True

    except Exception as e:
        error_msg = f'{e}'
    return NSLookupResult(target=target,success=success,response_body=response_body,duration=duration,error_msg=error_msg)
