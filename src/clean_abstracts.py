#!/usr/bin/env python3
"""Module to pre-processes PubMed/MedLine abstracts."""

import re
import pandas as pd
import argparse
from src.pubmed_countries import country_dict


def replace_country(x: pd.DataFrame) -> pd.DataFrame:
    """Search and replace values of a dataframe column.
    :param x: Pandas dataframe column (i.e., Country).
    :return x: Pandas dataframe column (i.e., Country) where values have been
        replaced with dictionary key.
    """
    for key in country_dict:
        for value in country_dict[key]:
            if value in x:
                return key
    return x


# remove html tags in abstracts and titles
def remove_html_tags(text: str) -> str:
    """Remove HTML-tags from a Pandas dataframe.
    :param text: Unprocessed text containing HTML-tags.
    :return text: Processed text where HTML-tags has been removed.
    """
    return re.sub('<[^<]+?>', '', str(text))


def preprocess_abstracts(raw_filename: str, clean_filename: str) -> None:
    """Pre-process the latest raw PubMed data.

    1) Remove duplicate rows.
    2) Remove rows with empty 'Abstract' fields.
    3) Set NaN/NA fields of 'Author', 'Title', 'Country', and 'Journal' to
       'Unknown'.
    4) set NA of 'Year' to 0 and convert the column to integers.
    5) Homogenize 'Country' by applying country replacement function to the
       dataframe.
    6) Remove HTML tags in 'Title' and 'Abstract' columns.
    7) Remove whitespaces in 'Title' and 'Abstract' columns.
    8) Reset dataframe index.

    Pre-processed CSV file is saved with the following naming convention:
    <date>_<clean_filename>.csv
    :param raw_filename: Raw filename without date or extension.
    :param clean_filename: Filename of the pre-processed file.
    """
    df = pd.read_csv(raw_filename)
    # remove duplicated rows
    df = df.drop_duplicates(subset={'Author', 'Title', 'Year', 'Country',
                                    'Journal', 'DOI', 'Abstract'})
    # remove NaN rows in 'Abstract'
    df.dropna(subset=['Abstract'], inplace=True)
    # set NaN/NA fields to 'Unknown'
    cols = ['Author', 'Title', 'DOI', 'Country', 'Journal']
    df[cols] = df[cols].fillna('Unknown')
    # set NA of 'Year' to 0
    df['Year'].fillna(0, inplace=True)
    # set year to integer
    df['Year'] = df['Year'].astype(int)
    # homogenize 'Country' by applying replacement function to the data frame
    df['Country'] = df['Country'].apply(lambda x: replace_country(x))
    # remove HTML tags in title and abstracts
    df['Abstract'] = df['Abstract'].apply(remove_html_tags)
    df['Title'] = df['Title'].apply(remove_html_tags)
    # remove white spaces in Title
    df['Title'] = df['Title'].str.strip()
    # remove white spaces in Abstracts
    df['Abstract'] = df['Abstract'].str.strip()
    # reset index
    df = df.reset_index(drop=True)
    # save file to csv
    df.to_csv(f'{clean_filename}', header=True, index=False)
    # for manually updating the list of constants:
    # (df['Country'].value_counts()).to_csv('country_cleanup.csv', header=True)
    print(f'Pre-processed file saved as: {clean_filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess PubMed abstracts')
    parser.add_argument('raw_filename', help='Enter valid path.')
    parser.add_argument('clean_filename', help='Enter CSV filename.')
    args = parser.parse_args()
    print(args.raw_filename)
    print(args.clean_filename)
    preprocess_abstracts(args.raw_filename, args.clean_filename)
