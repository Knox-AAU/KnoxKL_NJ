# P5-Project
Repository covering the knowledge layer for group Knox18

## Installing dependencies
Requires Python 3.x (64-Bit)

1. Install the requirements: 
    * `python3 -m pip install -r requirements.txt`
2. Install a model for spacy
    * REQUIRED - Small (16MB) - `python3 -m spacy download da_core_news_sm`
    * Medium (46MB) - `python3 -m spacy download da_core_news_md`
    * RECOMMENDED - Large (546MB) - `python3 -m spacy download da_core_news_lg`


## Env variables
In the root of the project a ".env" file should be created.
This contains all the environment/configuration values for the python program.
In the ".env" the variables are defined as so:  
variable="value"  
An example is: RDF_OUTPUT_FOLDER="./rdf_output/"
| Variables  | Description  |
|--:|:--|
| INPUT_DIRECTORY | The relative path (from project root) or absolute path to where the publication files are located, need to be suffixed with an `/` |
| OUTPUT_DIRECTORY | The relative path (from project root) or absolute path to where the processed publications will be moved, need to be suffixed with an `/` |
| ERROR_DIRECTORY | The relative path (from project root) or absolute path to where the files raising an exception will be moved, need to be suffixed with an `/` |
| RDF_OUTPUT_FOLDER | The relative path (from project root) or absolute path to where the outputted RDF file will be created, need to be suffixed with an `/`  |
| KNOX_18_NAMESPACE | The base namespace url resources from the Knox project  |
| OUTPUT_FORMAT | The format for the generated RDF file, example is "turtle", possible formats can be found at "https://rdflib.readthedocs.io/en/stable/plugin_parsers.html"  |
| OUTPUT_FILE_NAME | The file name of the RDF output  |
| TRIPLE_DATA_ENDPOINT | The endpoint for the REST API for the Data Layer, needs the whole information as string, example: "http://127.0.0.1:8080/update" |
