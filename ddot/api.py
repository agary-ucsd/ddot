import sys
import argparse
import bottle
import pandas as pd
from bottle import Bottle, HTTPError, request
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from ddot import Ontology
import tempfile
import os
import csv

path_this = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] += os.pathsep + os.path.join(path_this, '..')
print(os.environ["PATH"])
from ddot import generate_clixo_file

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

api = Bottle()


@api.get('/api/networks')
def get_networks():

    return 'get_networks complete'


@api.post('/api/ontology')
def upload_file():
    #=================
    # default values
    #=================
    alpha = 0.05
    beta = 0.5

    try:
        data = request.files.get('file')
    except Exception as e:
        raise HTTPError(500, e)

    if data and data.file:
        if (request.query.alpha):
            alpha = request.query.alpha

        if (request.query.beta):
            beta = request.query.beta

        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            f.write(data.file.read())
            f_name = f.name
            f.close()

        try:
            clixo_file = generate_clixo_file(f_name, alpha, beta)

            return_json = {}
            with open(clixo_file, 'r') as tsvfile:
                reader = csv.DictReader(filter(lambda row: row[0] != '#', tsvfile), dialect='excel-tab', fieldnames=['a', 'b', 'c', 'd'])
                counter = 0
                for row in reader:
                    return_json[counter] = [row.get('a'), row.get('b'), row.get('c'), row.get('d')]
                    counter += 1

                return return_json

        except OverflowError as ofe:
            print('Error with running clixo')


@api.post('/api/ontology')
def upload_file():
    #=================
    # default values
    #=================
    alpha = 0.05
    beta = 0.5

    try:
        data = request.files.get('file')
    except Exception as e:
        raise HTTPError(500, e)

    if data and data.file:
        if (request.query.alpha):
            alpha = request.query.alpha

        if (request.query.beta):
            beta = request.query.beta

        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            f.write(data.file.read())
            f_name = f.name
            f.close()

        try:
            clixo_file = generate_clixo_file(f_name, alpha, beta)

            with open(clixo_file, 'r') as f_saved:
                df = pd.read_csv(f_saved, sep='\t', engine='python', header=None, comment='#')
                print(df.columns)
                ont1 = Ontology.from_table(df, clixo_format=True, parent=0, child=1)

            ont_url, G = ont1.to_ndex(name='MODY',
                                      ndex_server='http://test.ndexbio.org',
                                      ndex_pass='scratch2',
                                      ndex_user='scratch2',
                                      layout='bubble-collect',
                                      visibility='PUBLIC')

            if ont_url is not None and len(ont_url) > 0 and 'http' in ont_url:
                uuid = ont_url.split('/')[-1]
                return 'File has been processed.  UUID:: %s \n' % uuid
            else:
                return 'File has been processed.  UUID: %s \n' % ont_url


            print('File has been processed: %s' % ont_url)

        except OverflowError as ofe:
            print('Error with running clixo')

    else:
        raise HTTPError(422, '**** FILE IS MISSING ****')

    return "Unable to complete process.  See stack message above."

# run the web server
def main():
    status = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?', type=int, help='HTTP port', default=8383)
    args = parser.parse_args()

    print 'starting web server on port %s' % args.port
    print 'press control-c to quit'
    try:
        server = WSGIServer(('0.0.0.0', args.port), api, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('exiting main loop')
    except Exception as e:
        exit_str = 'could not start web server: %s' % e
        print(exit_str)
        status = 1

    print('exiting with status %d', status)
    return status


if __name__ == '__main__':
    sys.exit(main())
