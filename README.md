# SpringerLink
Springerlink article collection

Document Access

Code Implementation
Web Scraper for SpringerLink data
Keywords: speech language therapy, speech language disorder, speech sound disorder, articulation disorder, speech intervention, language intervention, Auditory Discrimination, Auditory Processing Disorder, Phonological Awareness, Phonological Processes,Auditory Perception,Babbling, Motor Speech Disorder,Fluency, Morpheme,Phonology,Stuttering,Language Impairment,Speech-language Pathologist


This project is a Python script that scrapes metadata for research articles from the "https://link.springer.com/search/" website. 
It navigates through different keywords and issues, extracting details like article titles, authors, abstracts, and download links. This script is particularly useful for researchers and academics interested in compiling a dataset of journal article metadata.

Requirements
Python >= 3.6

Selenium

undetected_chromedriver

time (built-in module)

csv (built-in module)

Installation
Install the required Python packages using pip. Run the following command in your terminal:

pip install selenium undetected_chromedriver
Usage
To run the script, simply navigate to the directory containing the script and run:

'python splink.py'

I have attached downloaded data in SplinkCsvData folder, it has different csv files for every keywords and final mergerd file as 'merged_csv_data.csv' which has 19000 rows of data.

