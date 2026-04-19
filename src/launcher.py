
import argparse
import traceback, sys



import json



if __name__ == '__main__':
    # run as a program
    # from netcheck import probe_statuses
    from network_ping import get_status as get_ping_status
    from network_nslookup import get_status as get_nslookup_status
    from network_http_request import get_status as get_httprequest_status
elif '.' in __name__:
    # package
    # from .netcheck import probe_statuses
    from .network_ping import get_status as get_ping_status
    from .network_nslookup import get_status as get_nslookup_status
    from .network_http_request import get_status as get_httprequest_status
else:
    # included with no parent package
    # from netcheck import probe_statuses
    from network_ping import get_status as get_ping_status
    from network_nslookup import get_status as get_nslookup_status
    from network_http_request import get_status as get_httprequest_status








def call_parse_program():
    # return probe_statuses({'arglist_strict':False})
    with open("config.json") as f:
        config = json.load(f)
        results = []
        for target in config['PING_TARGETS']:
            result = get_ping_status(target)
            results.append(result)

        for target in config['DNS_TARGET']:
            result = get_nslookup_status(target)
            results.append(result)

        for target in config['HTTP_TARGETS']:
            result = get_httprequest_status(target)
            results.append(result)

        print('\n'.join(f'{r}' for r in results))

def call_test_program():
    msg = '''
hello, world!
    '''
    print(msg)
    return True




run_programs = {
    'netprobe': call_parse_program,
    'test': call_test_program,
}



def main():
    try:
        parser = argparse.ArgumentParser(
            description="Universal caller of mdmtoolsap-py utilities"
        )
        parser.add_argument(
            #'-1',
            '--program',
            choices=dict.keys(run_programs),
            type=str,
            required=True
        )
        args, args_rest = parser.parse_known_args()
        if args.program:
            program = '{arg}'.format(arg=args.program)
            if program in run_programs:
                run_programs[program]()
            else:
                raise AttributeError('program to run not recognized: {program}'.format(program=args.program))
        else:
            print('program to run not specified')
            raise AttributeError('program to run not specified')
    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro()"
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


if __name__ == '__main__':
    main()
