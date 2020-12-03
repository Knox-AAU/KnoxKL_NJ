from resources.term_frequency import TermFrequency
from typing import Dict, List
from knox_util import print
import json
from json import JSONEncoder
from environment.EnvironmentConstants import EnvironmentVariables as ev
from rest.DataRequest import send_word_count_to_db

class WordFrequencyHandler():

    def __init__(self) -> None:
        self.tf = TermFrequency()
        self.currentKey = ''
        self.word_frequencies_ready_for_sending = []
    
    def do_word_count_for_article(self, articleTitle: str, articleContent: str, extracted_from_list: List) -> None:
        self.currentKey = articleTitle
        self.tf.process(articleTitle, articleContent)

        extracted_from: str = self.__concatenate_extracted_from__(extracted_from_list)

        self.__convert_to_word_frequency_JSON_object__(extracted_from)

    def __concatenate_extracted_from__(self, path_list: List) -> str:
        ret_val: str = ''

        count_extracted_from_paths = len(path_list)
        current_count = 1
        for path in path_list:
            ret_val += path

            if count_extracted_from_paths > current_count:
                ret_val += ','
            current_count += 1
        
        return ret_val

    def __convert_to_word_frequency_JSON_object__(self, extracted_from: str):
        if self.currentKey == '':
            print(f'Could not convert to word frequency object because CurrentKey is <{self.currentKey}>, with termfrequence object <{self.tf}>', 'debug')
            pass
        
        frequencyData = self.tf[self.currentKey]
        frequencyObject = __WordFrequency__(self.currentKey, extracted_from, frequencyData)
        
        json_object = json.dumps(frequencyObject, cls=__WordFrequenctEncoder__, sort_keys=True, indent=4, ensure_ascii=False)

        self.word_frequencies_ready_for_sending.append(json_object)
        self.__reset_current_count__()

    def __reset_current_count__(self, hard_reset=False):
        self.tf = TermFrequency()
        self.currentKey = ''
        if hard_reset:
            self.word_frequencies_ready_for_sending = []

    
    def send_pending_counts(self, backup_file_name: str) -> bool:
        success: bool = False
        for word_count_json in self.word_frequencies_ready_for_sending:
            success: bool = send_word_count_to_db(word_count_json)
            if not success:
                print(f'Sending word count data to Data layer failed for <{word_count_json}>, stopping sending and creating back_up...', 'error')
                break

        if not success:
            self.__create_file_back_up__(backup_file_name)
    
    def __create_file_back_up__(self, file_name: str) -> None:
        error_dir: str = ev.instance.get_value(ev.instance.ERROR_DIRECTORY)
        file_path: str = error_dir + 'word_count_' + file_name

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('{\n')
            file.write('\t\"back_up\": [\n')
            count_max = len(self.word_frequencies_ready_for_sending)
            count_current = 1
            for sending_json in self.word_frequencies_ready_for_sending:
                file.write(sending_json)
                if count_current < count_max:
                    file.write(',')
                file.write('\n')
                count_current += 1

            file.write('\t]\n}')

class __WordFrequency__():
    
    def __init__(self, title: str, extracted_from: str, frequencyData: List) -> None:
        self.words: List = []
        for word in frequencyData:
            count = frequencyData[word]
            self.words.append(__Word__(word,count))

        self.articleTitle: str = title
        self.filepath: str = extracted_from
        self.totalwordsinarticle: int = len(self.words)

class __Word__():

    def __init__(self, word: str, word_count: int) -> None:
        self.word = word
        self.amount = word_count
    
class __WordFrequenctEncoder__(JSONEncoder):
    def default(self, o) -> None:
        return o.__dict__