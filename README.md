# Data Cleaning

An exercise using Python that looks at cleaning and summarizing a fictional viral sequence database for a virus using Pandas.

## Setup

1. Clone the repository:

```
git clone https://github.com/edecocke-uncc/data_cleaning.git
```

2. Go into the project folder:

```
cd data_cleaning
```

3. Activate the environment:

```
conda activate data_cleaning
```

## Run

```
python3 sequence_cleaner.py
```

## What it does

* Loads a fictional viral sequence dataset for a virus containing intentional duplicates and missing values
* Identifies and removes duplicate rows using `drop_duplicates()`
* Detects and handles missing values by dropping rows with absent quality scores and filling missing text fields with placeholder strings
* Ranks sequences by quality score and filters to retain only high-quality sequences above a 95% threshold
* Computes summary statistics including total unique sequences and localities represented

## Output

A `auroravirus9_cleaned.csv` file is written to the current directory after each run.
