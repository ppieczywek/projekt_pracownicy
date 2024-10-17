

from statistics import median, mean
import os
import json
from pydantic import BaseModel, Field, field_validator

# doadatkowe utrudnienie
# napisać program lokalnie a następnie dodać za pomocą biblioteki ArgsSparse umożliwiśc zewneterzne określanie parametrów
# python <sciezkapliku>/main.py --input_file pracownicy.json --output_file output.csv
# dodaj testy
# i dodaj jako repozytorium gita


import datetime


class Employee(BaseModel):
    imie: str
    nazwisko: str
    zarobki_brutto: float = Field(..., gt=0)
    dzial: str
    data_zatrudnienia: str

    @field_validator('dzial')
    def validate_dzial(cls, v):
        if v in ['HR', 'Finanse', 'IT', 'Sprzedaz']:
            return v
        else:
            raise ValueError("Error - value should be ...")

    @field_validator('data_zatrudnienia')
    def validate_data_zatrudnienia(cls, v):
        try:
            datetime.date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def read_employee_data(file_path):
    if isinstance(file_path, str) is False:
        raise TypeError

    with open(file_path, 'r', encoding="utf8") as input_file:
        data = json.load(input_file)

    validated_data = []
    for record in data:
        employee = Employee(**record)
        validated_data.append(employee)
    return validated_data


def get_salary_stats(emploee_data):
    salary = {}
    stats = {}
    for employee in emploee_data:
        if salary.get(employee.dzial, None) is None:
            salary[employee.dzial] = [employee.zarobki_brutto]
        else:
            salary[employee.dzial].append(employee.zarobki_brutto)
    for dzial, zarobki in salary.items():
        stats[dzial] = {'lower': 0.95*min(zarobki),
                        'upper': 1.10*max(zarobki),
                        'mean': mean(zarobki),
                        'median': median(zarobki)}
    return stats


def save_data(output_file, data):
    with open(output_file, 'w') as f:
        f.write(
            "dzial,srednia_wynagrodzen,mediana_wynagrodzen, dolne_widelki,gorne_widelki\n")
        for dzial, statystyki in data.items():
            f.write((f"{dzial}, {statystyki['mean']},"
                    f"{statystyki['median']},"
                     f"{statystyki['lower']},"
                     f"{statystyki['upper']}\n"))


if __name__ == "__main__":
    data = read_employee_data('.\src\employee_project\sample_data.json')
    stats = get_salary_stats(data)
    save_data("output.csv", stats)
