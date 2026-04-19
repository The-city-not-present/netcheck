
import argparse
import traceback, sys



# import json



if __name__ == '__main__':
    # run as a program
    from webserve import run
    from produce_html import render_page_home, render_page_test, render_page_performance, render_page_render_csv, render_page_about, render_page_netstats_refresh
elif '.' in __name__:
    # package
    from .webserve import run
    from .produce_html import render_page_home, render_page_test, render_page_performance, render_page_render_csv, render_page_about, render_page_netstats_refresh
else:
    # included with no parent package
    from webserve import run
    from produce_html import render_page_home, render_page_test, render_page_performance, render_page_render_csv, render_page_about, render_page_netstats_refresh




address = '0.0.0.0'
port_num = 8051
endpoints = {
    '/': render_page_home,
    '/test': render_page_test,
    '/perf': render_page_performance,
    '/net_stats_refresh': render_page_netstats_refresh,
    '/reader': render_page_render_csv,
    '/about': render_page_about,
}




def call_webserve_program():
    return run(address,port_num,endpoints)

def call_test_program():
    msg = '''
hello, world!
    '''
    print(msg)
    return True




run_programs = {
    'webserve': call_webserve_program,
    # 'test': call_test_program,
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
