

from dataclasses import dataclass


import urllib.request
import ssl
import certifi
# import re
import time


from .common_types import CheckResult

@dataclass(kw_only=True)
class HttpRequestResult(CheckResult):
    pass

def get_status(target):
    success = False
    response_body = None
    error_msg = None
    duration = None
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        time_start = time.perf_counter()
        with urllib.request.urlopen(target, timeout=5, context=context) as response:
            time_end = time.perf_counter()
            error_msg = response.reason
            response_body = response.read().decode("utf-8", errors="ignore")
            error_msg = response.reason
            if not error_msg:
                error_msg = None
            duration = (time_end - time_start) * 1
            success = 200 <= response.status < 400

    except urllib.error.HTTPError as e:
        # HTTP-level error (server responded)
        try:
            response_body = response.read().decode("utf-8", errors="ignore")
            error_msg = (
                f"HTTP Error code: {e.code}, "
                f"HTTP reason: {e.reason}, "
                f"Response body: {response_body}"
            )
        except:
            error_msg = f'{e}'

    except urllib.error.URLError as e:
        # Network-level failure
        try:
            error_msg = f'{"URL Error:"} {e.reason}'
        except:
            error_msg = f'{e}'
    except Exception as e:
        error_msg = f'{e}'
    return HttpRequestResult(target=target,success=success,response_body=response_body,duration=duration,error_msg=error_msg)
