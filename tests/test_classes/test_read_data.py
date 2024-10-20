from src.classes.employee import read_employee_data
import unittest


class TestReadEmployeeData(unittest.TestCase):
    def test_wrong_input_type(self):
        self.assertRaises(TypeError, read_employee_data, 123)

    def test_wrong_input_path(self):
        self.assertRaises(FileNotFoundError,
                          read_employee_data, "asdasd/123.json")

    def test_wrong_input_extension(self):
        self.assertRaises(ValueError, read_employee_data, "123.ssasad")
