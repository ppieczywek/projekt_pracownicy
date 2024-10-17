from src.classes.employee import get_salary_stats
import unittest


class TestGetSalaryStats(unittest.TestCase):
    def test_wrong_input_type(self):
        self.assertRaises(TypeError, get_salary_stats, 123)

    def test_wrong_input_list(self):
        self.assertRaises(AttributeError, get_salary_stats, [1, 2, 3])

    def test_empty_input_list(self):
        self.assertEquals(len(get_salary_stats([])), 0)
