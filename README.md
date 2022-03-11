# Azure Translator Interface

This project aims to test how well `Azure Translator` service performs when it comes to detect languages.

To do so, we will select text of the 5 most common languages from the [Wikipedia Language Identification Database](https://zenodo.org/record/841984), and compare the returned language label with the already known language label and ouput some scores.

The selected languages are: Mandarin Chinese (`zho`), Spanish (`spa`), English (`eng`), Arabic (`ara`), Hindi (`hin`).

## Installation

In order to use this project locally, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_AI_01.git
>>> cd OC_AI_01
```

### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```

## Notebook

The provided notebook offers to discover the various steps that led to the "Azure_Translator_Interface.py" python script

```bash
>>> jupyter notebook notebook.ipynb
```

## Running the project

Once installed, the project can be run in two different modes; one paragraph per request, or a batch of paragraph in each request.

#### One pararagraph at a time
```bash
>>> python3 Azure_Translator_Interface.py
```

In this mode, the app should should offer to input some text before connecting the Azure translator API in order to detect the language.
Finally, it will display the result and offer to input a new bloc on text.

#### A batch of pragraph
```bash
>>> python3 Azure_Translator_Interface.py -f PATH_TO_FILE EXPECTED_LABEL
>>> python3 Azure_Translator_Interface.py -f data/export_hin.txt hin
```
The `PATH_TO_FILE` should point to a file in which each line is considered as a paragraph.
The `EXPECTED_LABEL` is used to compute the accuracy and recall. It represents the expected label for the whole batch (up to 100 lines) and tt can be any of the following labels: 'ara', 'eng', 'hin', 'spa' or 'zho'

The app will connect to the Azure translator API in order to detect the language, and it will finally return several score and export the answers to `data/export_answers.json`
