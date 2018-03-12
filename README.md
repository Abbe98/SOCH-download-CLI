# SOCH Download CLI

![screenshot](screenshot.png)

SOCH Download CLI lets you do **multithreaded** batch downloads Swedish Open Cultural Heritage(K-Samsök) records for offline processing and analytics.

## Prerequirements

 - GIT
 - Python 3.6
 - [pipenv](https://docs.pipenv.org/)
 - An API key (get one by sending a email to ksamsok@raa.se)

## Installing

```bash
git clone https://github.com/riksantikvarieambetet/SOCH-download-CLI.git
cd SOCH-download-CLI
pipenv install
```

## Usage Examples

**Heads up: This program might use all the systems available CPUs.**

Download records based on a SOCH search query(Text, CQL, indexes, etc):

```bash
pipenv run python soch-download.py --key={API-KEY} --action=query --query=thumbnailExists=j
```

Download records from an specific institution(using the institution abbreviation):

```bash
pipenv run python soch-download.py --action=institution --institution=raa
```

Download records using a predefined action/query:

```bash
pipenv run python soch-download.py --action=all
pipenv run python soch-download.py --action=geodata-exists
```

List all available parameters and actions:

```bash
pipenv run python soch-download.py --help
```
