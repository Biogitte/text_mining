#!/usr/bin/env python3
"""Module to fetch PubMed abstracts based on a query"""
from Bio import Entrez
import csv
import time
import argparse

timestr = time.strftime('%Y%m%d')


def pubmed_search(email: str, query: str):
    """Search PubMed database.
    :param email: Valid email address in the format:
        <email>@<email>.<ext>. Email address is required ny NCBI.
    :param query: PubMed search-query in the format: 'search query'.
    :return results: Returns a data frame containing the following attributes:
    +------------+------------------------------------+
    |  Author    | Main author of the publication.    |
    +------------+------------------------------------+
    |  Title     | Publication title.                 |
    +------------+------------------------------------+
    |  Year      | Publication year.                  |
    +------------+------------------------------------+
    |  Country   | Publication country.               |
    +------------+------------------------------------+
    |  Journal   | Publication journal abbreviation.  |
    +------------+------------------------------------+
    |  DOI       | Digital Object Identifier (DOI)    |
    +------------+------------------------------------+
    |  Abstract  | Publication abstract.              |
    +------------+------------------------------------+
    Note: The retmax is set to 10.000 (i.e., the number of PubMed UIDs that will be included in the result).
    """
    Entrez.email = email
    search_handle = Entrez.esearch(db='pubmed', sort='relevance',
                                   retmax='10000', term=query)
    search_results = Entrez.read(search_handle)
    pubmed_id = search_results['IdList']
    id_list = ','.join(pubmed_id)
    print(f'The search found {len(id_list)} articles with the query {query}.')
    fetch_handle = Entrez.efetch(db='pubmed', retmode='xml', id=id_list)
    fetch_results = Entrez.read(fetch_handle)
    headers = ['Author', 'Title', 'Year', 'Country', 'Journal', 'DOI',
               'Abstract']
    results = [headers]
    for paper in fetch_results['PubmedArticle']:
        article = paper['MedlineCitation']['Article']
        try:
            name = article['AuthorList'][0]
            author = name['ForeName'] + ' ' + name['LastName']
        except (KeyError, IndexError):
            author = None
        try:
            title = article['ArticleTitle']
        except (KeyError, IndexError):
            title = None
        try:
            year = article['Journal']['JournalIssue']['PubDate']['Year']
        except (KeyError, IndexError):
            year = None
        try:
            affiliation = \
                article['AuthorList'][-1]['AffiliationInfo'][0]['Affiliation']
            country = affiliation[(affiliation.rfind(',')) + 2:][:-1]
        except (KeyError, IndexError):
            country = None
        try:
            journal = article['Journal']['ISOAbbreviation']
        except (KeyError, IndexError):
            journal = None
        try:
            doi = article['ELocationID'][1]
        except (KeyError, IndexError):
            doi = None
        try:
            abstract = article['Abstract']['AbstractText'][0]
        except (KeyError, IndexError):
            abstract = None

        features = [author, title, year, country, journal, doi, abstract]
        results.append(features)
    return results


def pubmed_abstracts_to_csv(data_dir: str, email: str, filename: str, query: str) -> None:
    """Create a csv with PubMed records based on a search query.
    :param data_dir: Data directory to host the abstracts.
    :param email: Valid email address in the format: <email>@<email>.<ext>.
        Email address is required by NCBI.
    :param filename: CSV filename in the format: '<filename>'
        (without csv extension).
    :param query: PubMed search-query in the format: 'search query'.
    :return <filename>.csv: containing PubMed records with the following
        attributes:
    +------------+------------------------------------+
    |  Author    | Main author of the publication.    |
    +------------+------------------------------------+
    |  Title     | Publication title.                 |
    +------------+------------------------------------+
    |  Year      | Publication year.                  |
    +------------+------------------------------------+
    |  Country   | Publication country.               |
    +------------+------------------------------------+
    |  Journal   | Publication journal abbreviation.  |
    +------------+------------------------------------+
    |  DOI       | Digital Object Identifier (DOI)    |
    +------------+------------------------------------+
    |  Abstract       | Publication abstract.         |
    +------------+------------------------------------+
    """
    with open(f'{data_dir}/{timestr}_{filename}.csv', 'w', newline='',
              encoding='UTF-8') as f:
        csv_writer = csv.writer(f, dialect='excel')
        raw_data = pubmed_search(email, query)
        for i in raw_data:
            csv_writer.writerow(i)
    return None


if __name__ == '__main__':
    descr = 'Retrieve PubMed abstracts to CSV file.'
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('data_dir', type=str, help='Enter data directory.')
    parser.add_argument('email', type=str, help='Enter valid e-mail address.')
    parser.add_argument('filename', type=str, help='Enter CSV filename.')
    parser.add_argument('query', type=str, help='Enter PubMed search keyword.')
    args = parser.parse_args()
    pubmed_abstracts_to_csv(args.data_dir, args.email, args.filename, args.query)