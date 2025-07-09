from flask import Flask, Response, request, make_response, render_template, redirect, url_for
import importlib
mtg_print = importlib.import_module("mtg-proxies-backend.print")
#from multiprocessing import Process
#from multiprocessing import Pipe
import multiprocessing
import secrets


app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


MAX_WORKERS = 3
workers = []
####conn1, conn2 = multiprocessing.Pipe()
queue = multiprocessing.Queue()

def get_message(connection):
    '''this could be any function that blocks until data is ready'''
    #time.sleep(1.0)
    #s = time.ctime(time.time())
    try:
        s = connection.recv()
        if len(s) == 0:
            s = ["",""]
    except EOFError:
        connection.close()
        s = ["",""]
    return s

def genPdfAsync(args, filename, queue, task_done_event):
    #pdf = bytes(str(mtg_print.genPdf(args, conn2).output(dest='S'), 'latin-1'), 'latin-1')
    mtg_print.genPdf(args, queue).output('./' + filename)
####    conn1.close()
####    conn2.close()
    task_done_event.set()
#    return pdf

@app.route('/generatePdf', methods=["GET", "POST"])
def generatePdf():
    global conn1
    global conn2

    if request.method == "POST":
        data = request.get_json()

        conn1, conn2 = multiprocessing.Pipe()
        intelligentBackground = '--no-intelligent_background'
        cropmarks = '--no-cropmarks'
        hSpace = 0
        vSpace = 0
        dpi = 300

        decklist = data['cards']
        intelligentBackgroundCB = request.form.get('intelligentBackground')
        cropmarksCB = request.form.get('cropmarks')

        if data['intelligentBackground'] == True:
            intelligentBackground = '--intelligent_background'
        if data['cropmarks'] == True:
            cropmarks = '--cropmarks'
        if len(data['hSpace']) > 0:
            try:
                hSpace = int(data['hSpace'])
            except ValueError:
                pass
        if len(data['vSpace']) > 0:
            try:
                vSpace = int(data['vSpace'])
            except ValueError:
                pass
        if len(data['dpi']) > 0:
            try:
                dpi = int(data['dpi'])
            except ValueError:
                pass

        print("dpi: " + str(dpi))
        args=['--border_crop', '0', '--dpi', str(dpi), intelligentBackground, cropmarks, '--directInput', '--directOutput', '--hSpace', str(hSpace), '--vSpace', str(vSpace), decklist, './testprint.pdf']

        filename = 'print_' + request.cookies.get('token') + '.pdf'

        for worker_process, task_done_event in workers:
            if task_done_event.is_set():
                task_done_event.clear()
                workers.remove((worker_process, task_done_event))

        if len(workers) < MAX_WORKERS:
            task_done_event = multiprocessing.Event()
            pdfProcess = multiprocessing.Process(target=genPdfAsync, args=(args, filename, queue, task_done_event))
            pdfProcess.start()
            workers.append((pdfProcess, task_done_event))

        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': "attachment;filename=print.pdf"
        }
        return {'success': True}
    return {'success': False}

@app.route('/downloadPdf', methods=["GET", "POST"])
def downloadPdf():
    #print("Download method activaterd!")
    #return {'success': True}

    filename = 'print_' + request.cookies.get('token') + '.pdf'

    try:
        #pdf_file = open('/mnt/Storage/Share/' + filename, "r", encoding='latin-1')
        pdf_file = open('./' + filename, "rb")
    except FileNotFoundError:
        #response = make_response(render_template("index.html"))
        #return response
        return redirect(url_for('index'))

    pdf = pdf_file.read()
    #pdf = bytes(pdf_file.read(), 'latin-1') # if you only wanted to read 512 bytes, do .read(512)
    pdf_file.close()

    #headers = {
    #    'Content-Type': 'application/pdf',
    #    'Content-Disposition': "attachment;filename=print.pdf"
    #}

    #return Response(pdf, headers=headers)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'print'
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    response = make_response(render_template("index.html"))
    response.set_cookie('token', secrets.token_hex(16))
    return response


@app.route('/stream')
def stream():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
####            data = get_message(conn1)
            data = queue.get(block=True)
            yield 'data: {}\n\n'.format(data[0]+":"+data[1])
    return Response(eventStream(), mimetype="text/event-stream")

app.run(host='0.0.0.0', port=9093)
