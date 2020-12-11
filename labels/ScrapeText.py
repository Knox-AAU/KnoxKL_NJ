from environment.EnvironmentConstants import EnvironmentVariables as ev
ev()
from knox_source_data_io.io_handler import IOHandler, Generator, Wrapper
from loader.JsonWrapper import Publication, Article, Paragraph
import spacy
import glob

def get_folder_files_list(path:str) -> list:
    """
    Outputs a list of files from the directory given.
    """

    filelist = glob.glob(path)

    return filelist

def read_json_file(path:str) -> str:
    '''Reads a specified json files following the Publication format and returns the text as a string'''

    handler = IOHandler(Generator(app='This app', version=1.0), 'https://repos.knox.cs.aau.dk/schema/publication.schema.json')
    with open(path, 'r', encoding='utf-8') as json_file:
        wrap: Wrapper = handler.read_json(json_file)
        publication: Publication = wrap.content
        text = ''
        for article in publication.articles:
            text = ' '.join(para.value for para in article.paragraphs if para.value is not None)

    return text

def read_txt_file(path:str) -> str:
    '''Reads and returns the text of a file'''
    with open(path, 'r', encoding='utf-8') as source:
        text = source.read()


    return text

def write_model_entities(inputtext:str):
    '''
    Writes the entities in the inputtext into the file specified.
    The format written is the one used my train_model.py    
    '''
    nlp = spacy.load('Path to spaCy model')

    with open(r'Path to write annotated training data.', 'w', encoding='utf-8') as target:
        target.write('TRAIN_DATA = [')

        temp = nlp(inputtext.replace('\n', ' '))
        sentences = temp.sents
        for sentence in sentences:
            doc = nlp(sentence.text)
            if len(doc.ents) > 0:

# The training data for new entities in the current implementation must be of a certain format.
# Be in a [(<sentence>, {'entities':, [(<entity start index>, <entity end index>, <entity label>)}])]
# Where multiple entities can be tagged in the same sentence.

                target.write('(\''+sentence.text.replace('\'', '\\\'')+'\', {\'entities\': [')
                found_entities = []
                temp_dict: dict = {}
                for ent in doc.ents:
                    if ent.text in found_entities:
                        continue

                    found_entities.append(ent.text)
                    ent_length = len(ent.text)
                                
                    index_list = find_matches(ent.text, sentence.text, temp_dict)
    
                    for j in index_list:
                        target.write('(' + str(j)+ ', ' + str(j + ent_length) + ', ' + '\'' + ent.label_ +'\')')
    
                        if j != index_list[-1] or doc.ents[-1] != ent:
                            target.write(', ')
    
                target.write(']}),\n')
    
        target.write(']')

def find_matches(search_string: str, search_text: str, last_matches: dict) -> list:
    '''Finds matches in the recognized entities'''
    index_list = []

    last_search = last_matches.get(search_string, 0)
    next_index = search_text.find(search_string, last_search)
    while next_index != -1:
        index_list.append(next_index)
        next_val = next_index + len(search_string)
        last_matches.update({search_string: next_val})

        last_search = next_val
        next_index = search_text.find(search_string, last_search)
    
    return index_list
