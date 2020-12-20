# P5-Project
Repository covering the knowledge layer for group Knox18

## Installing dependencies
Requires Python 3.8.x (64-Bit)

1. Install the requirements: 
    * `python3 -m pip install -r requirements.txt`
2. Install a model for spacy
    * Small (16MB) - `python3 -m spacy download da_core_news_sm`
        * Does not contain word vectors
    * Medium (46MB) - `python3 -m spacy download da_core_news_md`
    * REQUIRED - Large (546MB) - `python3 -m spacy download da_core_news_lg`

### Adding Knox specific packages

In order to install Knox specific packages in your projects, you must first add the knox package repository to your pip indexes. The index can either be specified on every `pip install`, or be configured in a configuration file.

To simply specify an extra index on `pip install`, run the the following command:

```
pip install --extra-index-url https://repos.knox.aau.dk your packages here
```

To add the repostory to your repository indexes, paste the following into your pip configuration file

```ini
[global]
extra-index-url = https://repos.knox.cs.aau.dk/
```

#### Cofiguration files (Windows)

For Windows the following configuration files should be available. If they are not available you can create them.

* `~/pip/pip.ini`
* `./venv/pip.ini`

#### Configuration files (Linux)

For Linux the following configuration files should be available. If they are not available you can create them.

* `~/.pip/pip.conf`
* `./venv/pip.conf`

## Env variables
In the root of the project a `.env` file should be created.
This contains all the environment/configuration values for the python program.
In the `.env` the variables are defined as so:  
variable="value"  
An example is: `RDF_OUTPUT_FOLDER="./rdf_output/"`

| Variable Name  | Description  |
|--|--|
| `INPUT_DIRECTORY` | The relative path (from project root) or absolute path to where the publication files are located, need to be suffixed with an `/` |
| `OUTPUT_DIRECTORY` | The relative path (from project root) or absolute path to where the processed publications will be moved, need to be suffixed with an `/` |
| `ERROR_DIRECTORY` | The relative path (from project root) or absolute path to where the files raising an exception will be moved, need to be suffixed with an `/` |
| `RDF_OUTPUT_FOLDER` | The relative path (from project root) or absolute path to where the outputted RDF file will be created, need to be suffixed with an `/`  |
| `OUTPUT_FORMAT` | The format for the generated RDF file, example is "turtle", possible formats can be found at "https://rdflib.readthedocs.io/en/stable/plugin_parsers.html"  |
| `OUTPUT_FILE_NAME` | The file name of the RDF output  |
| `ONTOLOGY_FILEPATH` | The path to the ontology file |
| `TRIPLE_DATA_ENDPOINT` | The triple data endpoint for the REST API for the Data Layer, needs the whole information as string, example: "http://127.0.0.1:8080/update" |
| `WORD_COUNT_DATA_ENDPOINT` | The word count endpoint for the REST API for the Data Layer, needs the whole information as string, example: "http://127.0.0.1:8080/wordCountData" |
| ``
