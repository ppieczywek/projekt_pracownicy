from src.classes.employee import save_data
import unittest


class TestSaveData(unittest.TestCase):

    def test_wrong_data_type(self):
        self.assertRaises(TypeError, save_data, '123.csv', 123)

    def test_wrong_output_type(self):
        data = {'HR': {'lower': 123,
                       'upper': 123,
                       'mean': 123,
                       'median': 123}}
        self.assertRaises(TypeError, save_data, 123, data)

    def test_wrong_data_dict(self):
        data = {'HR': {'asdas': 123,
                       'upper': 123,
                       'mean': 123,
                       'median': 123}}
        self.assertRaises(KeyError, save_data, '123.csv', data)

    def test_wrong_output_extesion(self):
        data = {'HR': {'lower': 123,
                       'upper': 123,
                       'mean': 123,
                       'median': 123}}
        self.assertRaises(ValueError, save_data, "123.txt", data)

    def test_wrong_output_path(self):
        data = {'HR': {'lower': 123,
                       'upper': 123,
                       'mean': 123,
                       'median': 123}}
        self.assertRaises(FileNotFoundError, save_data, "asdasd/123.csv", data)
