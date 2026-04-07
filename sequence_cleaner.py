#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Erin Nicole Decocker
# edecocke@charlotte.edu
# ID: 801442694

"""
sequence_cleaner.py

Cleans and summarizes a fictional viral sequence database. The dataset intentionally contains duplicate rows
and missing values.
"""
import pandas as pd

class TheVirusWrangler:
    """
    Loads, cleans, filters, and summarizes a viral sequence DataFrame.
    """

    def __init__(self, data: dict):
        """
        Initialises the raw viral sequence DataFrame from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing sequence metadata. Expected keys are
            'Sequence_ID', 'Locality', 'Sequenced_At', 'Repository_Link',
            and 'Quality(%)'.

        Ensures
        -------
        self.df is a valid pandas DataFrame containing the raw input data
        including any duplicates or missing values present in the source.
        self.df_high_quality is initialised as None until
        filter_by_quality() is called.

        Returns
        -------
        None
        """
        self.df = pd.DataFrame(data)
        self.df_high_quality = None

    def inspect_the_carnage(self) -> None:
        """
        Prints the raw DataFrame and an initial missing value report
        to assess data quality before any cleaning is performed.

        df.isnull().sum() counts the number of missing values per column,
        which is the recommended first step before deciding whether to
        drop or fill missing entries.

        Parameters
        ----------
        None

        Ensures
        -------
        Output shows the complete raw DataFrame, total duplicate count,
        and missing value counts per column.

        Returns
        -------
        None
        """
        print(f"\n{'-'*85}")
        print("Raw DataFrame")
        print(f"{'-'*85}")
        print(self.df)
        print(f"\nNumber of duplicate rows : {self.df.duplicated().sum()}")
        print(f"\nMissing values per column:")
        print(self.df.isnull().sum())

    def purge_the_duplicates(self) -> None:
        """
        Identifies and removes fully duplicated rows from the DataFrame.

        df.drop_duplicates() retains the first occurrence of each
        duplicated row and discards all subsequent copies. This step
        is necessary because duplicate entries would skew summary
        statistics and inflate sequence counts.

        Parameters
        ----------
        None

        Ensures
        -------
        self.df is modified in place to contain only unique rows.
        The row count before and after removal is printed.

        Returns
        -------
        None
        """
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        print(f"\n{'-'*60}")
        print("Duplicate Removal")
        print(f"{'-'*60}")
        print(f"  Rows before : {before}")
        print(f"  Rows after  : {after}")
        print(f"  Removed     : {before - after}")

    def handle_the_missing_mayhem(self) -> None:
        """
        Handles missing values by dropping rows with missing quality
        scores and filling missing text fields with placeholder strings.

        Two strategies are applied in sequence:
        1. df.dropna(subset=['Quality(%)']) removes any row where the
           quality score is absent, as quality is required for filtering.
        2. df.fillna() replaces remaining missing text fields with
           'Unknown' or 'Unavailable' so downstream analysis is not
           disrupted by NaN entries in non-critical columns.

        Parameters
        ----------
        None

        Ensures
        -------
        self.df contains no missing values after this method completes.
        Rows with a missing 'Quality(%)' value are removed entirely.
        Missing 'Locality', 'Sequenced_At', and 'Repository_Link'
        values are replaced with descriptive placeholder strings.

        Returns
        -------
        None
        """
        self.df = self.df.dropna(subset=['Quality(%)'])
        self.df = self.df.fillna({
            'Locality': 'Unknown',
            'Sequenced_At': 'Unknown',
            'Repository_Link': 'Unavailable'
        })
    def rank_and_filter_the_worthy(self, threshold: float = 95.0) -> pd.DataFrame:
        """
        Sorts the cleaned DataFrame by quality score in descending order
        and retains only sequences meeting the minimum quality threshold.

        Parameters
        ----------
        threshold : float
            Minimum quality percentage required to retain a sequence.
            Defaults to 95.0.

        Ensures
        -------
        self.df is sorted by 'Quality(%)' in descending order.
        self.df_high_quality contains only rows where 'Quality(%)'
        is greater than or equal to the threshold value.

        Returns
        -------
        pd.DataFrame
            Filtered DataFrame containing only high-quality sequences.
        """
        self.df = self.df.sort_values(by='Quality(%)', ascending=False)
        self.df_high_quality = self.df[self.df['Quality(%)'] >= threshold]

        print(f"\n{'-'*100}")
        print(f"High-Quality Sequences (Quality >= {threshold}%)")
        print(f"{'-'*100}")
        print(self.df_high_quality)
        return self.df_high_quality

    def summarize_the_survivors(self) -> None:
        """
        Computes and prints summary statistics for the high-quality
        sequence dataset including unique sequence and locality counts.

        nunique() counts the number of distinct values in a Series,
        which is appropriate here for counting unique sequence identifiers
        and unique collection localities without manual deduplication.

        Parameters
        ----------
        None

        Ensures
        -------
        rank_and_filter_the_worthy() must be called before this method.
        Output reports the total number of unique high-quality sequences
        and the total number of unique localities represented.

        Returns
        -------
        None
        """
        total_sequences = self.df_high_quality['Sequence_ID'].nunique()
        total_localities = self.df_high_quality['Locality'].nunique()

        print(f"\n{'-'*60}")
        print("Summary Statistics")
        print(f"{'-'*60}")
        print(f"Total unique high-quality sequences : {total_sequences}")
        print(f"Total unique localities represented : {total_localities}")
        print(f"\nQuality(%) descriptive statistics:")
        print(self.df_high_quality['Quality(%)'].describe().round(2))

    def export_to_csv(self, filename: str = "auroravirus9_cleaned.csv") -> None:
        """
        Exports the cleaned and filtered high-quality DataFrame to a CSV file.

        Parameters
        ----------
        filename : str
            Output file path. Defaults to 'auroravirus9_cleaned.csv'
            in the current working directory.

        Ensures
        -------
        The CSV file is written without the integer row index.
        rank_and_filter_the_worthy() must be called before this method
        so that only high-quality sequences are exported.

        Returns
        -------
        None
        """
        self.df_high_quality.to_csv(filename, index=False)

if __name__ == "__main__":

    data = {
        'Sequence_ID': [
            'AURV9_001', 'AURV9_002', 'AURV9_003', 'AURV9_004',
            'AURV9_005', 'AURV9_006', 'AURV9_002', 'AURV9_007', 'AURV9_008',
            'AURV9_009', 'AURV9_010', 'AURV9_003'
        ],
        'Locality': [
            'Sao Paulo, Brazil', 'Tokyo, Japan', 'Nairobi, Kenya', 'Berlin, Germany',
            'Cape Town, South Africa', None, 'Tokyo, Japan', 'Reykjavik, Iceland',
            'Toronto, Canada', 'Lima, Peru', 'Delhi, India', 'Nairobi, Kenya'
        ],
        'Sequenced_At': [
            'USP Genomics Core', 'Riken Institute', 'Kenya BioLab', 'Max Planck Institute',
            'UCT Genomics Center', 'Unknown', 'Riken Institute', 'Arctic Viral Lab',
            'Toronto Genomics Hub', None, 'Delhi Biotech Center', 'Kenya BioLab'
        ],
        'Repository_Link': [
            'https://db.aurora.org/AURV9_001', 'https://db.aurora.org/AURV9_002',
            'https://db.aurora.org/AURV9_003', 'https://db.aurora.org/AURV9_004',
            None, 'https://db.aurora.org/AURV9_006', 'https://db.aurora.org/AURV9_002',
            'https://db.aurora.org/AURV9_007', 'https://db.aurora.org/AURV9_008',
            'https://db.aurora.org/AURV9_009', 'https://db.aurora.org/AURV9_010',
            'https://db.aurora.org/AURV9_003'
        ],
        'Quality(%)': [
            99.8, 97.2, 92.5, 96.1, 88.9, 100.0, 97.2, 94.3,
            99.5, None, 91.8, 92.5
        ]
    }

    wrangler = TheVirusWrangler(data=data)
    wrangler.inspect_the_carnage()
    wrangler.purge_the_duplicates()
    wrangler.handle_the_missing_mayhem()
    wrangler.rank_and_filter_the_worthy(threshold=95.0)
    wrangler.summarize_the_survivors()
    wrangler.export_to_csv("auroravirus9_cleaned.csv")
