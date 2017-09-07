from unittest import TestCase
import deep_mapper


DATA = {
    'root': [
        {'title': 'hello', 'counter': 1, 'media': {'ico': 'http://example.com'}},
        {'title': 'world', 'counter': 2, 'media': {}},
        {'title': 'Im', 'counter': '3'},
        {'title': 'here'},
    ]
}


class TestDMapper(TestCase):

    def test_only_exist_keys(self):
        MAP_STRUCTURE = {
            'name': {'path': '/title'},
        }
        result = deep_mapper.process_mapping(DATA, MAP_STRUCTURE, '/root')
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) == len(DATA['root']))
        self.assertTrue(result[0]['name'] == DATA['root'][0]['title'])

    def test_with_various_empty_keys(self):
        MAP_STRUCTURE = {
            'name': {'path': '/title'},
            'image': {'path': '/media/ico'},
        }
        result = deep_mapper.process_mapping(DATA, MAP_STRUCTURE, '/root')
        self.assertTrue(isinstance(result, list))

    def test_postprocess(self):
        MAP_STRUCTURE = {
            'name': {'path': '/title'},
            'count': {'path': '/counter', 'postprocess': int},
            'image': {'path': '/media/ico'},
        }
        result = deep_mapper.process_mapping(DATA, MAP_STRUCTURE, '/root')
        self.assertTrue(isinstance(result, list))