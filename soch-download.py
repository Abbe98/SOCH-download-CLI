import re
import math
import click
import requests
import glob

from ksamsok import KSamsok

actions = [
    'geodata-exists',
    'all',
    'institution',
    'query',
]
action_help = ', '.join(actions)

headers = {
    'User-Agent': 'SOCH Download CLI',
}

api_key = 'test'

def build_query(query, hits, start):
    return 'http://www.kulturarvsdata.se/ksamsok/api?x-api={3}&method=search&query={0}&hitsPerPage={1}&startRecord={2}'.format(query, hits, start, api_key)

def fetch(query, n_requests):
    target_queries = list()
    count = 0
    while n_requests != len(target_queries):
        click.echo(len(target_queries))
        start_record = len(target_queries) * 500
        url = build_query(query, 500, start_record)
        target_queries.append(url)

    click.echo(target_queries)

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
    click.echo('Would you like to proceed with the download? y/n')
    c = click.getchar()
    if c == 'y':
        click.echo('Preparing download')
        return fetch(query, required_n_requests)

    exit()

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
@click.option('--key', default='test', help='SOCH API key')
@click.option('--institution', help='The institution abbreviation (Only applies if action=institution).')
def start(action, key, institution):
    click.secho('Validating arguments...', fg='yellow')
    try:
        auth = KSamsok(key)
        api_key=key
    except:
        error('Bad API key.')

    if action not in actions:
        error('Unknown action.')

    # note: using glob instead of os.listdir because it ignores dotfiles
    if glob.glob('data/*'):
        error('The data directory is not empty.')

    if action == 'institution':
        if not institution:
            error('Institution action given without specified institution.')
        confirm('serviceOrganization=' + institution)
    elif action == 'all': confirm('*')
    elif action == 'geodata-exists': confirm('geoDataExists=j')

if __name__ == '__main__':
    start()
