
import argparse
import traceback, sys
from datetime import datetime, timezone
from pathlib import Path
import os # for getsize - checking if file is empty
import csv
from dataclasses import asdict



import json



if __name__ == '__main__':
    # run as a program
    from utility_perfmonitor import PerformanceMonitor
    from utility_taskqueue import TaskQueue
    from network_ping import get_status as get_ping_status
    from network_nslookup import get_status as get_nslookup_status
    from network_http_request import get_status as get_httprequest_status
elif '.' in __name__:
    # package
    from .utility_perfmonitor import PerformanceMonitor
    from .utility_taskqueue import TaskQueue
    from .network_ping import get_status as get_ping_status
    from .network_nslookup import get_status as get_nslookup_status
    from .network_http_request import get_status as get_httprequest_status
else:
    # included with no parent package
    from utility_perfmonitor import PerformanceMonitor
    from utility_taskqueue import TaskQueue
    from network_ping import get_status as get_ping_status
    from network_nslookup import get_status as get_nslookup_status
    from network_http_request import get_status as get_httprequest_status



def program_netcheck(config):
    try:
        time_start = datetime.now()
        parser = argparse.ArgumentParser(
            description="Netcheck",
            prog='netcheck'
        )
        parser.add_argument(
            '-1',
            '--config',
            help='Config file',
            type=str,
            required=True
        )
        parser.add_argument(
            '-2',
            '--output',
            help='Output csv',
            type=str,
            required=True
        )
        # parser.add_argument(
        #     '--config-something',
        #     help='Config: some config',
        #     type=str,
        #     choices = ["somethinga","somethingb"],
        #     required=False
        # )
        args = None
        args_rest = None
        if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
            args, args_rest = parser.parse_known_args()
        else:
            args = parser.parse_args()

        input_file = None
        if args.config:
            input_file = Path(args.config)
            input_file = '{input_file}'.format(input_file=input_file.resolve())
        else:
            raise FileNotFoundError('Inp source: file not provided; please use --file')

        if not(Path(input_file).is_file()):
            raise FileNotFoundError('file not found: {fname}'.format(fname=input_file))

        output_file = None
        if args.output:
            output_file = Path(args.output)
            output_file = '{output_file}'.format(output_file=output_file.resolve())
        else:
            raise FileNotFoundError('Inp source: file not provided; please use --file')
        out_file_exists = Path(output_file).is_file()
        if out_file_exists:
            if os.path.getsize(output_file) == 0:
                out_file_exists = False


        config = {
        }
        # if args.config_something:
        #     config['xxx'] = yyy

        print('Netcheck script: script started at {dt}'.format(dt=time_start))

        with open(input_file) as f:
            print(f'Netcheck script: with config file "{input_file}"')
            config = json.load(f)
            q = TaskQueue()
            for target in config['PING_TARGETS']:
                q.add_task(target, request_type='ping')
            for target in config['DNS_TARGET']:
                q.add_task(target, request_type='dns_lookup')
            for target in config['HTTP_TARGETS']:
                q.add_task(target, request_type='http')

            results = []
            performance_counter = iter(PerformanceMonitor(config={
                'total_records': q.count(),
                'report_frequency_records_count': 1,
                'report_frequency_timeinterval': 0.0001,
            }))
            while q.count() > 0:
                # task = q.get_next_task()
                task = q.get_next_task(meta_filter=lambda m: m.get('request_type', 0) == 'ping')
                if task is None:
                    break
                next(performance_counter)
                result = get_ping_status(task.payload)
                results.append(result)

            while q.count() > 0:
                # task = q.get_next_task()
                task = q.get_next_task(meta_filter=lambda m: m.get('request_type', 0) == 'dns_lookup')
                if task is None:
                    break
                next(performance_counter)
                result = get_nslookup_status(task.payload)
                results.append(result)

            while q.count() > 0:
                # task = q.get_next_task()
                task = q.get_next_task(meta_filter=lambda m: m.get('request_type', 0) == 'http')
                if task is None:
                    break
                next(performance_counter)
                result = get_httprequest_status(task.payload)
                results.append(result)

            if q.count() > 0:
                raise Exception('Error: something left in the queue')




            # print('\n'.join(f'{r}' for r in results))

            print(f'Netcheck script: Writing results to "{output_file}"')
            with open(output_file, "a", newline="", encoding="utf-8") as file:
                fieldnames = ["target", "created_at", "success", "duration", "error_msg", "response_body"]
                def clean(record):
                    record = {**record}
                    response_body = record['response_body']
                    response_body = f'{response_body}'
                    if len(response_body)>64:
                        response_body = response_body[:62]+'...'
                    response_body = json.dumps(response_body)
                    record['response_body'] = response_body
                    error_msg = record['error_msg']
                    error_msg = f'{error_msg}'
                    if len(error_msg)>128:
                        error_msg = error_msg[:126]+'...'
                    error_msg = json.dumps(error_msg)
                    record['error_msg'] = error_msg
                    return record
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header only if file is new
                if not out_file_exists:
                    writer.writeheader()
                writer.writerows(clean(asdict(record)) for record in results)



            print('Netcheck script: finished')

        time_finish = datetime.now()
        print('Netcheck script: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start))
    except Exception as e:
        # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write 'print('File Not Found!');exit(1);', I just write 'raise FileNotFoundErro()'
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print('{e}'.format(e=e),file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)
