import glob
import math
import re
import shutil
import sys
import time

import click
import requests
from ksamsok import KSamsok

import background

actions = [
    'geodata-exists',
    'all',
    'institution',
    'query',
    'color-exists',
    'keyword-exists',
]
action_help = ', '.join(actions)

bar = None

headers = {
    'User-Agent': 'SOCH Download CLI',
}

api_key = 'test'

def build_query(query, hits, start):
    return 'http://www.kulturarvsdata.se/ksamsok/api?x-api={3}&method=search&query={0}&hitsPerPage={1}&startRecord={2}'.format(query, hits, start, api_key)

@background.task
def fetch(url, start_record):
    bar.update(0)
    filepath = 'raw_data/' + str(start_record) + '.xml'
    # streaming and copying file object to save memory
    r = requests.get(url, headers=headers, timeout=None, stream=True)

    with open(filepath, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    bar.update(1)

def pre_fetch(query, n_requests):
    global bar
    with click.progressbar(length=n_requests, label='Downloading...') as bar:
        # because the progress bar is updated from other threads
        # we clear it here so it's not duplicated
        sys.stdout.write('\x1b[2K\x1b[1A')

        count = 0
        while n_requests > count:
            start_record = count * 500
            fetch(build_query(query, 500, start_record), start_record)
            count += 1

        # the sleep is used for performance reasons
        while not bar.finished:
            time.sleep(0.5)
        click.secho('\nDone!', fg='green', nl=False)

def confirm(query):
    click.secho('Fetching query data and calculating requirements...', fg='green')

    target = build_query(query, 1, 0)
    r = requests.get(target, headers=headers)
    n_results = int(re.search(r'<totalHits>(\d+?)<\/totalHits>', r.text).group(1))

    if not valid_http_status(r.status_code):
        error('SOCH returned an error. \n' + target)

    if n_results == 0:
        error('SOCH returned zero records. \n' + target)

    required_n_requests = math.ceil(n_results / 500)

    click.echo('Found {0} results, they would be split over {1} requests/files'.format(n_results, required_n_requests))
    click.echo('This program might use all the systems available CPUs({0})!'.format(background.n))
    click.echo('Would you like to proceed with the download? y/n')
    c = click.getchar()
    if c == 'y':
        click.secho('Preparing download...', fg='green')
        return pre_fetch(query, required_n_requests)

    exit()

def unpack_xml():
    click.secho('Starting unpacking...', fg='green')
    if not glob.glob('raw_data/*'):
        error('The data directory is empty, nothing to unpack.')

    if glob.glob('rdf_data/*'):
        error('The RDF data directory is not empty')

    with click.progressbar(glob.glob('raw_data/*.xml'), label='Unpacking') as bar:
        for xml in bar:
            save_rdf(xml)

    time.sleep(1)
    click.secho('Done!', fg='green')
    exit()

record_pattern = re.compile(r'<record>((.|\n)+?)<\/record>')

def save_rdf(filepath):
    contents = None
    n = None
    with open(filepath, 'r') as f:
        n = re.search(r'(\d+)', filepath).group(1)
        contents = f.read()

    for i, find in enumerate(re.finditer(record_pattern, contents)):
        rdf = find.group(1)
        rdf = re.sub(r'<rel:score.+$', '', rdf)
        rdf = '<?xml version="1.0" encoding="UTF-8"?>' + rdf
        with open('rdf_data/' + n + '_' + str(i) + '.rdf', 'w', encoding='utf-8') as f:
            f.write(rdf)

def valid_http_status(status):
    if 200 <= status <= 399:
        return True
    else:
        return False

def error(text):
    click.secho(text, err=True, fg='red')
    exit()

@click.command()
@click.option('--action', default='all', help=action_help)
@click.option('--key', default='test', help='SOCH API key.')
@click.option('--institution', help='The institution abbreviation (Only applies if action=institution).')
@click.option('--query', help='SOCH search query string (Only applies if action=query).')
@click.option('--unpack', default=False, is_flag=True, help='Unpacks the XML downloads into RDF files.')
def start(action, key, institution, query=False, unpack=False):
    click.secho('Validating arguments...', fg='yellow')

    if unpack:
        unpack_xml()

    global api_key
    try:
        auth = KSamsok(key)
        api_key=key
    except:
        error('Bad API key.')

    if action not in actions:
        error('Unknown action.')

    # note: using glob instead of os.listdir because it ignores dotfiles
    if glob.glob('raw_data/*'):
        error('The raw data directory is not empty.')

    if action == 'institution':
        if not institution:
            error('Institution action given without specified institution.')
        confirm('serviceOrganization=' + institution)
    elif action == 'query':
        if not query:
            error('Query action given without specified query.')
        confirm(query)
    elif action == 'all': confirm('*')
    elif action == 'geodata-exists': confirm('geoDataExists=j')
    elif action == 'color-exists': confirm('itemColor=*')
    elif action == 'keyword-exists': confirm('itemKeyWord=*')

if __name__ == '__main__':
    start()
