import html
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import csv
import html


import subprocess
import re



if __name__ == '__main__':
    # run as a program
    import html_template as report_html_template
elif '.' in __name__:
    # package
    from . import html_template as report_html_template
else:
    # included with no parent package
    import html_template as report_html_template



def render(result_ins_htmlmarkup_title,result_ins_htmlmarkup_heading,report_htmlmarkup_mainpart_with_tables):

    result_ins_htmlmarkup_headertext = 'webserve'

    result_template = '{begin}{report_contents}{end}'.format(
        begin = report_html_template.TEMPLATE_HTML_BEGIN,
        report_contents = '{{INS_MAIN_PART}}',
        end = report_html_template.TEMPLATE_HTML_END
    )

    result = result_template
    result = result.replace(
        '{{INS_TITLE}}', result_ins_htmlmarkup_title
    )
    result = result.replace(
        '{{INS_PAGEHEADER}}', result_ins_htmlmarkup_headertext
    )
    result = result.replace(
        '{{INS_REPORTTYPE}}', 'all'
    )
    result = result.replace(
        '{{INS_HEADING}}', result_ins_htmlmarkup_heading
    )
    result = result.replace(
        '{{INS_BANNER}}', '<!-- banners --><style>.mdmreport-banner-global { display: none; }</style>'
    )
    prefix_replacement = '{{INS_MAIN_PART}}'
    prefix_end = result.index(prefix_replacement)
    postfix_begin = prefix_end + len(prefix_replacement)
    result = result[:prefix_end] + report_htmlmarkup_mainpart_with_tables + result[postfix_begin:]

    return result, 'text/html'

def render_page_home(requested_path, handler_instance):
    return render('Home','Welcome!','<p>Welcome here!</p>')

def render_page_test(requested_path, handler_instance):
    return render('Test page','Test','<p>Test page.</p>')

def render_page_performance(requested_path, handler_instance):
    commands = [
        ['uname','-a',],
        ['uptime',],
        ['cat','/proc/loadavg',],
        ['cat','/proc/meminfo',],
        ['lscpu',],
        ['cat','/proc/cpuinfo',],
        ['top','-o','cpu','-l','1','-n','20',],
        ['free','-h',],
        ['df','-h',],
        ['du','-h','/',],
        ['ps','aux',],
    ]
    results = []
    for command in commands:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
            )

            response_body = result.stdout
            error_msg = result.stderr
            if not error_msg:
                error_msg = None
            results.append((' '.join(command),response_body,error_msg,))
        except Exception as e:
            results.append((' '.join(command),'',f'{e}',))

    def prep_markup(command,response_body,error_msg):
        part_wrapper_begin = f'<section class="mdmreport-banner">'
        part_wrapper_end = f'</section>'
        part_1_command = f'<div class="command"><pre>{command}</pre></div>'
        part_2_body = f'<div class="command-output"><pre>{response_body}</pre></div>'
        part_3_errors = f'<div class="command-err error"><pre>{error_msg}</pre></div>' if error_msg else ''
        parts_total = f'{part_wrapper_begin}{part_1_command}{part_2_body}{part_3_errors}{part_wrapper_end}'
        return parts_total

    return render(
        'Performance statistics',
        'Performance statistics',
        ''.join([prep_markup(command,response_body,error_msg) for command,response_body,error_msg in results])
    )

def render_page_netstats_refresh(requested_path, handler_instance):
    commands = [
        ['python','/root/netcheck/netcheck.py','--program','netprobe','--config','config.json','--output','connectivity_log.csv'],
    ]
    results = []
    for command in commands:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
            )

            response_body = result.stdout
            error_msg = result.stderr
            if not error_msg:
                error_msg = None
            results.append((' '.join(command),response_body,error_msg,))
        except Exception as e:
            results.append((' '.join(command),'',f'{e}',))

    def prep_markup(command,response_body,error_msg):
        part_wrapper_begin = f'<section class="mdmreport-banner">'
        part_wrapper_end = f'</section>'
        part_1_command = f'<div class="command"><pre>{command}</pre></div>'
        part_2_body = f'<div class="command-output"><pre>{response_body}</pre></div>'
        part_3_errors = f'<div class="command-err error"><pre>{error_msg}</pre></div>' if error_msg else ''
        parts_total = f'{part_wrapper_begin}{part_1_command}{part_2_body}{part_3_errors}{part_wrapper_end}'
        return parts_total

    return render(
        'Action: refresh netstats',
        'Action: refresh netstats',
        ''.join([prep_markup(command,response_body,error_msg) for command,response_body,error_msg in results])
    )

def render_page_render_csv(requested_path, handler_instance):
    trusted_dirs = ['/root/netcheck/','/Users/andrej/work/netmonitor/dist']
    def is_within_directory(file_path: str, directory: str) -> bool:
        file_path = Path(file_path).resolve()
        directory = Path(directory).resolve()

        try:
            file_path.relative_to(directory)
            return True
        except ValueError:
            return False

    parsed = urlparse(requested_path)
    path = parsed.path          # "/some/path"
    query = parsed.query        # "a=1&b=2"

    params = parse_qs(query)    # {'a': ['1'], 'b': ['2']}

    file = params.get('file',None)
    if not file or not (len(file)>0):
        raise Exception('file is not provided!')
    file = file[0]
    file = Path(file).resolve()
    is_within_any_directory = False
    for p in trusted_dirs:
        is_within_any_directory = is_within_any_directory or is_within_directory(file,p)
    if not is_within_any_directory:
        raise Exception('the requested file is not in trusted location')
    if not (file.suffix=='.csv'):
        raise Exception('the requested file type is not allowed')
    if not file.is_file():
        raise FileNotFoundError(f'the requested file does not exist ({file})')

    # Open the CSV file
    results = ''
    with open(file, newline='') as csvfile:
        # Create a CSV reader
        reader = csv.reader(csvfile)

        # Iterate over each row
        header_row = None
        rows = []
        for i,row in enumerate(reader):
            r = ''
            added_css = ' mdmreport-record-header' if i==0 else ''
            r += f'<tr class="mdmreport-record{added_css}">'
            for cell in row:
                cell_clean = f'{cell}'
                is_datetime = re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*',cell_clean)
                cell_clean = html.escape(cell)
                if is_datetime:
                    cell_clean = f'<span data-role="date">{cell_clean}</span>'
                r += f'<td class="mdmreport-contentcell">{cell_clean}</td>'
            r += '</tr>'
            if i>0:
                rows.append(r)
            else:
                header_row = r
    results += header_row
    for row in reversed(rows):
        results += row

    resp_body = report_html_template.TEMPLATE_HTML_TABLE_BEGIN.replace('{{TABLE_ID}}','csv').replace('{{TABLE_NAME}}','csv').replace('{{INS_TABBANNER}}','')+results+report_html_template.TEMPLATE_HTML_TABLE_END

    return render('Display CSV',f'{file}',resp_body)

def render_page_visitor_inspect(requested_path, handler_instance):
    client_ip = handler_instance.client_address[0]
    response = ''
    response += f'<tr class="mdmreport-record mdmreport-record-header"><td class="mdmreport-contentcell">Key</td><td class="mdmreport-contentcell">Value</td></tr>'
    response += f'<tr class="mdmreport-record"><td class="mdmreport-contentcell">client_ip</td><td class="mdmreport-contentcell">{html.escape(client_ip)}</td></tr>'
    for key, value in handler_instance.headers.items():
        if 'x-forwarded-for'.lower() in key.lower():
            response += f'<tr class="mdmreport-record"><td class="mdmreport-contentcell">{html.escape(key)}</td><td class="mdmreport-contentcell">{html.escape(value)}</td></tr>'
    for key, value in handler_instance.headers.items():
        if 'x-forwarded-for'.lower() not in key.lower():
            response += f'<tr class="mdmreport-record"><td class="mdmreport-contentcell">{html.escape(key)}</td><td class="mdmreport-contentcell">{html.escape(value)}</td></tr>'
    resp_body = report_html_template.TEMPLATE_HTML_TABLE_BEGIN.replace('{{TABLE_ID}}','headers').replace('{{TABLE_NAME}}','HTTP Headers').replace('{{INS_TABBANNER}}','')+response+report_html_template.TEMPLATE_HTML_TABLE_END
    return render('Welcome!',f'Welcome, {client_ip}',resp_body)

def render_page_about(requested_path, handler_instance):
    return render('Aboud','About me','<p>Andrey 2026.</p>')
