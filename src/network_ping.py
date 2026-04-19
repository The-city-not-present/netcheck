

from dataclasses import dataclass


import subprocess
import re


from .common_types import CheckResult

@dataclass(kw_only=True)
class PingResult(CheckResult):
    pass

def get_status(target):
    def parse_request_time(output):
        results = []
        output_lines = output.split('\n')
        for line in output_lines:
            try:
                match = re.search(r"time=([0-9.]+)", line)
                if match:
                    captured = match.group(1)
                    captured_num = float(captured)
                    captured_num = captured_num / 1000 # to seconds, from ms
                    results.append(captured_num)
            except:
                pass
            try:
                match = re.search(r"(?:round-trip|trr)\b.*?=\s*(.*)", line)
                if match:
                    captured = match.group(1)
                    captured = captured.split('/')
                    captured = captured[1] # avg
                    captured_num = float(captured)
                    captured_num = captured_num / 1000 # to seconds, from ms
                    results.append(captured_num)
                    captured = match.group(1)
                    captured = captured.split('/')
                    captured = captured[2] # max
                    captured_num = float(captured)
                    captured_num = captured_num / 1000 # to seconds, from ms
                    results.append(captured_num)
            except:
                pass
        return sum(results) / len(results) if results else float('nan')
    # def parse_packets_received(output):
    #     results = []
    #     output_lines = output.split('\n')
    #     for line in output_lines:
    #         try:
    #             match = re.search(r"packets transmitted,\s*(\d+)\s*packets received", line)
    #             if match:
    #                 captured = match.group(1)
    #                 captured_num = int(captured)
    #                 results.append(captured_num)
    #         except:
    #             pass
    #     result = 0
    #     if results:
    #         result = sum(results) / len(results)
    #         if result>0:
    #             result = int(result)
    #             if result>0:
    #                 return result
    #             else:
    #                 return 1 # keep incidence, not round to 0 if it's positive
    #         else:
    #             return 0
    success = False
    response_body = None
    error_msg = None
    duration = None
    try:
        result = subprocess.run(
            ["ping", "-c", "1", target],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if True:
            response_body = result.stdout
            error_msg = result.stderr
            if not error_msg:
                error_msg = None
            # packets_received = parse_packets_received(response_body)
            duration = parse_request_time(response_body)
            success = (result.returncode == 0) # and (packets_received>0) and not result.stderr

    except Exception as e:
        error_msg = f'{e}'
    return PingResult(target=target,success=success,response_body=response_body,duration=duration,error_msg=error_msg)
