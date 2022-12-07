#!/usr/bin/env python3
"""Module to pre-processes PubMed/MedLine abstracts."""
import re
import pandas as pd
import argparse
import glob
import os
from src.pubmed_countries import country_dict


def find_latest_csv(input_dir: str) -> str:
    """
    Returns the path to the newest CSV file of a given input directory.
    :param input_dir: Input directory path.
    """
    list_of_files = glob.glob(f"{input_dir}/*.csv")
    latest_csv = max(list_of_files, key=os.path.getctime)
    return latest_csv


def get_base_name(path: str) -> str:
    """
    Get the base name of a file or directory
    :param path: Path to file or directory
    :return name: Base name of file or directory
    """
    if os.path.isfile(path):
        name = os.path.splitext(os.path.basename(path))[0]
        return name
    elif os.path.isdir(path):
        name = os.path.basename(path)
        return name
    else:
        return "File or directory does not exist"


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


def remove_html_tags(text: str) -> str:
    """Remove HTML-tags from a Pandas dataframe.
    :param text: Unprocessed text containing HTML-tags.
    :return text: Processed text where HTML-tags has been removed.
    """
    return re.sub('<[^<]+?>', '', str(text))


def preprocess_abstracts(input_dir: str, out_dir: str, input_file=None, output_file=None) -> None:
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

    :param input_dir: Input directory.
    :param out_dir: Output directory.
    :param input_file: Optional input filename (i.e., only filename - not path).
                       If not given, the newest CSV file of the input directory will be used.
    :param output_file: Optional filename of the pre-processed file (i.e., only filename - not path).
                        If not given, it will create a file name based on the newest CSV file in the
                         input directory and add a "_clean" to the end before the CSV extension.
    """

    if input_file is None:
        input_path = find_latest_csv(input_dir)
    else:
        input_path = f"{input_dir}/{input_file}"

    df = pd.read_csv(input_path)

    df = df.drop_duplicates(subset={'Author', 'Title', 'Year', 'Country',
                                    'Journal', 'DOI', 'Abstract'})
    df.dropna(subset=['Abstract'], inplace=True)
    cols = ['Author', 'Title', 'DOI', 'Country', 'Journal']
    df[cols] = df[cols].fillna('Unknown')
    df['Year'].fillna(0, inplace=True)
    df['Year'] = df['Year'].astype(int)
    df['Country'] = df['Country'].apply(lambda x: replace_country(x))
    df['Abstract'] = df['Abstract'].apply(remove_html_tags)
    df['Title'] = df['Title'].apply(remove_html_tags)
    df['Title'] = df['Title'].str.strip()
    df['Abstract'] = df['Abstract'].str.strip()
    df = df.reset_index(drop=True)

    if output_file is None:
        basename = get_base_name(input_path)
        out_path = f"{out_dir}/{basename}_clean.csv"
    else:
        out_path = f"{out_dir}/{output_file}"
    df.to_csv(f'{out_path}', header=True, index=False)

    # for manually updating the list of constants:
    #(df['Country'].value_counts()).to_csv('country_cleanup.csv', header=True)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess PubMed abstracts')
    parser.add_argument('input_dir', help='Enter valid path.')
    parser.add_argument('out_dir', help='Enter valid path.')
    parser.add_argument('input_file', nargs='?', help='Enter CSV filename (not path).')
    parser.add_argument('output_file', nargs='?', help='Enter CSV filename (not path).')
    args = parser.parse_args()
    preprocess_abstracts(args.input_dir, args.out_dir, args.input_file, args.output_file)
