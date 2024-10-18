from src.classes.employee import read_employee_data
from src.classes.employee import save_data
from src.classes.employee import get_salary_stats


class Project:

    def __init__(self, input, output) -> None:
        self.input = input
        self.output = output

    def process(self) -> None:
        data = read_employee_data(self.input)
        stats = get_salary_stats(data)
        save_data(self.output, stats)
