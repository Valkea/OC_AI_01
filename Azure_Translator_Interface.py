#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to detect the language
    of provided texts using the Azure Translator API.
"""

import argparse
import requests
import uuid
import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np


# ----- PREPARE API REQUESTS -----

# Load API 'subscription_key' and 'endpoint' from non commited file
with open("secrets.txt", "r") as secrets:
    subscription_key = secrets.readline().strip()
    endpoint = secrets.readline().strip()


# Prepare the parameters for the API's requests
location = "francecentral"
path = "/detect"
constructed_url = endpoint + path
params = {"api-version": "3.0"}
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}


# ----- ONE-LINE INPUT -----


def detect_one_paragraph(input_txt):
    """Formats the input text to fit the Azure Translator API, send the request and return the json result.

    Parameters
    ----------
    input_txt: string
         The paragraph for which one wants to know the language name according to Azure translator.

    """

    body = [{"text": input_txt}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    return request.json()


def input_loop():
    """Offers to input a paragraph to detect,
    detect the language and start all over.
    """

    input_text = input("\nPlease input your text: ")

    result = detect_one_paragraph(input_text)
    print(f"ANSWER: {result}\n")

    another = input("Detect another paragraph? [y|N] ")
    if another.lower() == "y":
        input_loop()
    else:
        sys.exit(0)


# ----- BATCH FILE INPUT -----


def prepare_lines(path):
    """Open the provided file and format its lines to fit the Azure Translator API.

    Parameters
    ----------
    path: string
         The path to the file containing the sample paragraphs.
    """

    try:
        with open(path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(0)

    max_batch_size = 100
    max_characters = 50000

    inputs = []
    count_chars = 0

    for line in lines:

        count_chars += len(line)
        if count_chars > max_characters:
            print("The batch has reached the max characters limit")

        inputs.append({"text": line})

        if len(inputs) == max_batch_size:
            break

    print(
        f"This batch containes {count_chars} characters distributed on {len(inputs)} lines\n"
    )
    return inputs


def parse_batch_results(responses, lang):
    """Use the results provided by Azure Translator to compute and display some metrics.

    Parameters
    ----------
    response: string
        The results provided by Azure Translator API.
    lang: string
        The label of the expected language for this batch.
    """

    valid_answer_labels = {
        "zho": ["lzh", "zh-Hans", "zh-Hant"],
        "eng": ["en"],
        "spa": ["es"],
        "ara": ["ar"],
        "hin": ["hi"],
        "fra": ["fr", "fr-ca"],
    }

    # Convert to Dataframe and add/remove columns
    results = pd.DataFrame(responses)
    results["label"] = lang
    results = results.drop(
        ["isTranslationSupported", "isTransliterationSupported"], axis="columns"
    )

    for i, r in results.iterrows():
        results["isOk"] = r["language"] in valid_answer_labels[r["label"]]

    # Print Dataframe
    print(results, "\n")

    # Print some metrics
    average_azure_score = results["score"].mean()
    print(f"Average Azure score:{average_azure_score}")

    average_local_score = np.sum(results["isOk"]) / len(results)
    print(f"Average local score:{average_local_score}")

    TP = np.sum(results["isOk"])
    FN = len(results) - TP
    recall = TP / (TP + FN)
    print(f"Recall score: {recall}")


def detect_batch(args):
    """Check the provided arguments, gets the batch file content, send it to the Azure Translator API and display results.

    Parameters
    ----------
    args: dict
        The first element of this dict provides the batch file path.
        The second element of this dict provides the expected language label.
    """

    path = args[0]
    lang = args[1]

    if lang not in ["ara", "eng", "hin", "spa", "zho"]:
        print("The provided language label is not supported.")
        print("Please us any of the following: 'ara', 'eng', 'hin', 'spa', 'zho'")
        sys.exit(0)

    print(f'\nLet\'s try to detect "{lang}" sentences.')

    body = prepare_lines(path)

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    results = request.json()

    # FAKE RESULTS
    # results = [
    #     {
    #         "language": "en",
    #         "score": 0.97,
    #         "isTranslationSupported": True,
    #         "isTransliterationSupported": False,
    #     },
    #     {
    #         "language": "en",
    #         "score": 0.98,
    #         "isTranslationSupported": True,
    #         "isTransliterationSupported": False,
    #     },
    # ]

    # Compute scores
    parse_batch_results(results, lang)

    # Save json to file
    json_path = Path("data", "export_answers.json")
    json_string = json.dumps(results)
    with open(json_path, "w+") as file:
        file.write(json_string)

    print(f"\n>> The results are saved in {json_path}\n")


if __name__ == "__main__":

    """The main function parse the arguments and call the appropriate functions."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--paragraph",
        action="store_true",
        help="Send one paragraph to Azure Translator",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        nargs="+",
        help="Send the content of one file to Azure Translator",
    )

    args = parser.parse_args()

    if args.file:
        detect_batch(args.file)
    else:
        input_loop()
