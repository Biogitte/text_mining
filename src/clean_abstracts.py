#!/usr/bin/env python3
"""Module to pre-process PubMed/MedLine textual data (i.e., abstracts) for text mining/NLP."""
import re
import glob
import os
import string
import time
import spacy
import warnings
import pandas as pd
from typing import Union
import argparse
from num2words import num2words


warnings.filterwarnings(action='ignore', category=UserWarning)

from src.pubmed_countries import country_dict

timestr = time.strftime('%Y%m%d')
nlp = spacy.load('en_core_sci_lg')
# nlp.add_pipe('abbreviation_detector')


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
    """
    if os.path.isfile(path):
        name = os.path.splitext(os.path.basename(path))[0]
        return name
    elif os.path.isdir(path):
        name = os.path.basename(path)
        return name
    else:
        return "File or directory does not exist"


def load_csv_data(path: str) -> Union[pd.DataFrame, str]:
    """Import latest CSV file from directory OR a specific CSV file if path is given.
    :param path: path to directory with CSV files OR path to a single CSV file.
    """
    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df
    elif os.path.isdir(path):
        latest_csv = find_latest_csv(path)
        df = pd.read_csv(latest_csv)
        return df
    else:
        return "File or directory does not exist"


def replace_country(x: pd.DataFrame) -> pd.DataFrame:
    """Search and replace values  (i.e., Countries) of a dataframe column.
    :param x: Pandas dataframe column (i.e., Country).
    """
    for key in country_dict:
        for value in country_dict[key]:
            if value in x:
                return key
    return x


def remove_html_tags(text: str) -> str:
    """Remove HTML-tags from a Pandas dataframe.
    :param text: Unprocessed text containing HTML-tags.
    """
    return re.sub('<[^<]+?>', '', str(text))


def numbers_to_txt(text: str) -> str:
    """
    Convert numbers to text using num2words.
    :param text: Input text data.
    """
    text = re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text)
    return text


def remove_numbers(text: str) -> str:
    """
    Remove numbers from text.
    :param text: Input text data.
    """
    text = re.sub(r'\d+', '', text)
    return text


def remove_punctuations(text: str) -> str:
    """
    Remove punctuations, accent marks and diacritics from text.
    :param text: Input text data.
    """
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# TODO: Fix abbreviation functionality (sci-spacy vs. spark versions clash)
# def convert_abbreviations(text: str) -> str:
    #     """
    #   Convert abbreviations to text using SciSpacy.
    #   :param text: Input text data.
    #   """
    #   doc = nlp(text)
    #   altered_tok = [tok.text for tok in doc]
    #   for abrv in doc._.abbreviations:
#    altered_tok[abrv.start] = str(abrv._.long_form)
#  return (" ".join(altered_tok))


def abstract_prep(input_dir: str, out_dir: str, replace_numbers=True, output_file=None) -> None:
    """
    Pre-process and normalize raw PubMed/Medline data for NLP.
    1) Import latest CSV file in a directory - or a specific CSV file from input path.
    2) Remove duplicate rows.
    2) Remove rows with empty 'Abstract' fields.
    3) Set NaN/NA fields of 'Author', 'Title', 'Country', and 'Journal' to
       'Unknown'.
    4) set NA of 'Year' to 0 and convert the column to integers.
    5) Homogenize 'Country' by applying country replacement function to the
       dataframe.
    6) Remove HTML tags in 'Title' and 'Abstract' columns.
    7) Convert numbers into words (True) or remove numbers (False) in 'Abstract' column.
    8) Expand abbreviations with SciSpacy language model (medium) in 'Abstract' column.
    9) Remove punctuations in 'Abstract' column.
    10) Convert text to lowercase in 'Abstract' column.
    11) Remove whitespaces in 'Title' and 'Abstract' columns.
    12) Reset dataframe index.
    13) Save the preprocessed CSV file.
    """
    df = load_csv_data(input_dir)

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

    if replace_numbers:
        df['Abstract'] = df['Abstract'].apply(numbers_to_txt)
    else:
        df['Abstract'] = df['Abstract'].apply(remove_numbers)

    # df['Abstract'] = df['Abstract'].apply(convert_abbreviations)

    df['Abstract'] = df['Abstract'].apply(remove_punctuations)

    df['Abstract'] = df['Abstract'].str.lower()

    df['Title'] = df['Title'].str.strip()
    df['Abstract'] = df['Abstract'].str.strip()
    df = df.reset_index(drop=True)

    if output_file is None:
        input_path = find_latest_csv(input_dir)
        basename = get_base_name(input_path)
        out_path = f"{out_dir}/{basename}_clean.csv"
    else:
        out_path = f"{out_dir}/{output_file}"

    df.to_csv(f'{out_path}', header=True, index=False)

    # for manually updating the list of country constants:
    # (df['Country'].value_counts()).to_csv(f'{out_dir}/country_cleanup.csv', header=True)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess PubMed/Medline abstracts')
    parser.add_argument('input_dir', help='Enter valid path.')
    parser.add_argument('out_dir', help='Enter valid path.')
    parser.add_argument('replace_numbers', nargs='?', help='Set to True if replacing numbers with word is wanted.')
    parser.add_argument('output_file', nargs='?', help='Enter CSV filename (not path).')
    args = parser.parse_args()
    abstract_prep(args.input_dir, args.out_dir, args.replace_numbers, args.output_file)