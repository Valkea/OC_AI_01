#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to detect the language
    of provided texts using the Azure Translator service.
'''

import argparse
import requests
import uuid

# Load API subscription_key and endpoint from non commited file
with open("secrets.txt", "r") as secrets:
    subscription_key = secrets.readline().strip()
    endpoint = secrets.readline().strip()


# Prepare request to API
location = "francecentral"
path = '/detect'
constructed_url = endpoint + path
params = {'api-version': '3.0'}
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def detect_one_paragraph(txt):
    """ Docstring TODO """
    body = [{'text': txt}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    return request.json()


def input_loop():
    """ Docstring TODO """
    input_text = input("\nPlease input your text: ")
    result = detect_one_paragraph(input_text)
    print(f"ANSWER: {result}\n")
    another = input("Detect another paragraph? [y|N] ")
    if another.lower() == 'y':
        input_loop()
    else:
        print("Close")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--paragraph', action='store_true', help="Send one paragraph to Azure Translator")

    args = parser.parse_args()

    print(args)
    if args.paragraph:
        input_loop()
    else:
        print("Bah...")
