from environment.EnvironmentConstants import EnvironmentVariables as ev
ev()
import os
import pytest
from extractor.WordFrequencyHandler import WordFrequencyHandler
import json


xfail = pytest.mark.xfail

class Test:
    
    def test_do_word_count_for_article(self):
        # Setup
        handler = WordFrequencyHandler()
        test_title = 'title_key'
        test_content = 'This is awesome content from an article'
        test_extracted_list = ['FromHere', 'ViaThis', 'ToThere']

        # Confirm clear
        assert len(handler.word_frequencies_ready_for_sending) == 0
        assert len(handler.tf[test_title]) == 0

        handler.do_word_count_for_article(test_title, test_content, test_extracted_list)

        assert len(handler.word_frequencies_ready_for_sending) == 1

        handler.do_word_count_for_article(test_title, test_content, test_extracted_list)
        handler.do_word_count_for_article(test_title, test_content, test_extracted_list)
        handler.do_word_count_for_article(test_title, test_content, test_extracted_list)
        handler.do_word_count_for_article(test_title, test_content, test_extracted_list)

        assert len(handler.word_frequencies_ready_for_sending) == 5

#

    def test___concatenate_extracted_from__empty_list(self):
        # Setup
        test_extracted_list = []
        handler = WordFrequencyHandler()
        expected = ''

        actual = handler.__concatenate_extracted_from__(test_extracted_list)
        assert actual == expected

    def test___concatenate_extracted_from__single_entry(self):
        # Setup
        test_extracted_list = ['FromHere']
        handler = WordFrequencyHandler()
        expected = 'FromHere'

        actual = handler.__concatenate_extracted_from__(test_extracted_list)
        assert actual == expected

    def test___concatenate_extracted_from__multiple_entries(self):
        # Setup
        test_extracted_list = ['FromHere', 'ViaThis', 'ToThere']
        handler = WordFrequencyHandler()
        expected = 'FromHere,ViaThis,ToThere'

        actual = handler.__concatenate_extracted_from__(test_extracted_list)
        assert actual == expected

#

    def test___convert_to_word_frequency_JSON_object__(self):
        # Setup
        handler = WordFrequencyHandler()
        test_title = 'title_key'
        test_content = 'This is awesome content'
        test_extract_file = 'Extracted from here'
        distinct_word_count = len(set(test_content.lower().split(' ')))
        handler.tf.process(test_title, test_content)
        handler.currentKey = test_title

        assert len(handler.word_frequencies_ready_for_sending) == 0
        handler.__convert_to_word_frequency_JSON_object__(test_title, test_extract_file)

        assert len(handler.word_frequencies_ready_for_sending) == 1
        json_string = handler.word_frequencies_ready_for_sending[0]
        
        json_object = json.loads(json_string)
        assert json_object['articleTitle'] == test_title
        assert json_object['totalwordsinarticle'] == distinct_word_count

#

    def test___reset__(self):
        # Setup
        handler = WordFrequencyHandler()
        test_title = 'title_key'
        test_content = 'This is awesome content'
        distinct_word_count = len(set(test_content.lower().split(' ')))
        handler.word_frequencies_ready_for_sending.append(test_title)

        # Confirm empty
        assert len(handler.tf[test_title]) == 0

        handler.tf.process(test_title, test_content)

        assert len(handler.tf[test_title]) == distinct_word_count
        assert len(handler.word_frequencies_ready_for_sending) > 0

        handler.__reset__()
        # Confirm empty
        assert len(handler.tf[test_title]) == 0
        assert len(handler.word_frequencies_ready_for_sending) > 0

    def test___reset__hard_reset(self):
        handler = WordFrequencyHandler()
        test_title = 'title_key'
        test_content = 'This is awesome content'
        distinct_word_count = len(set(test_content.lower().split(' ')))
        handler.word_frequencies_ready_for_sending.append(test_title)

        # Confirm empty
        assert len(handler.tf[test_title]) == 0

        handler.tf.process(test_title, test_content)

        assert len(handler.tf[test_title]) == distinct_word_count
        assert len(handler.word_frequencies_ready_for_sending) > 0

        handler.__reset__(True)
        # Confirm empty
        assert len(handler.tf[test_title]) == 0
        assert len(handler.word_frequencies_ready_for_sending) == 0

#

    def test_send_pending_count(self):
        # Setup
        handler = WordFrequencyHandler()
        test_title = 'title_key'
        test_content = 'This is awesome content'
        back_up_file_name = 'thisistestfilefortestingtest_send_pending_count.json'

        handler.tf.process(test_title, test_content)
        # Check that something exists
        counts = handler.tf[test_title]
        assert len(counts) == 4
        
        handler.send_pending_counts(back_up_file_name)

        # Expect to fail because of a Connection error
        # This triggers writing to a file
        error_dir = ev.instance.get_value(ev.instance.ERROR_DIRECTORY, './')
        file_path = error_dir + handler.back_up_file_prefix + back_up_file_name
        abs_path = os.path.abspath(file_path)
        
        assert os.path.exists(abs_path)

        # Cleanup
        os.remove(abs_path)
#

    def test___create_file_back_up__(self):
        # Setup
        error_dir = './err/'
        test_file = 'thisIsSpecificForTest__create_file_back_up__.json'
        handler = WordFrequencyHandler()

        handler.__create_file_back_up__(test_file, error_dir)

        abs_path = os.path.abspath(error_dir + handler.back_up_file_prefix + test_file)
        assert os.path.exists(abs_path)

        with open(abs_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            assert '{\n' in content
            assert '\t\"back_up\": [\n' in content
            assert '\t]\n' in content
            assert '}' in content
        # Clean up
        os.remove(abs_path)
