from typing import List, Dict
from statistics import median, mean
from pydantic import BaseModel, Field, field_validator
import json
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


def read_employee_data(file_path: str) -> List[Employee]:
    """Read employees data from JSON file.

    Args:
        file_path (str): path to JSON file

    Returns:
        List[Employee]: returns list of Employee class objects
    """
    if isinstance(file_path, str) is False:
        raise TypeError("Expected string with input file path")

    if file_path.endswith((".json")) is False:
        raise ValueError("Extension must be .json")

    with open(file_path, 'r', encoding="utf8") as input_file:
        data = json.load(input_file)

    validated_data = []
    for record in data:
        employee = Employee(**record)
        validated_data.append(employee)
    return validated_data


def get_salary_stats(employees_data: List[Employee]) -> Dict:
    """
    Calculates salary statistics in relation to the 
    company's department. Calculated statistics are: median salary, 
    mean salary, upper limit of salary, lower limit of salary.

    Args:
        employees_data (List[Employee]): 
        List of Employee class objects.

    Returns:
        Dict: 
        Dictionary of salary statistics calculated in relation 
        to the company's department.

    """
    if isinstance(employees_data, list) is False:
        raise TypeError("Expected list of Employee class objects")

    try:
        salary_data = {}
        stats = {}
        for employee in employees_data:
            if salary_data.get(employee.dzial, None) is None:
                salary_data[employee.dzial] = [employee.zarobki_brutto]
            else:
                salary_data[employee.dzial].append(employee.zarobki_brutto)
        for division, salary in salary_data.items():
            stats[division] = {'lower': 0.95*min(salary),
                               'upper': 1.10*max(salary),
                               'mean': mean(salary),
                               'median': median(salary)}
        return stats

    except AttributeError as e:
        raise AttributeError(f"Wrong dictionary key: {e}")


def save_data(output_file: str, data: dict) -> None:
    """
    Saves salary statitstics into csv file.

    Args:
        output_file (str):
        Path to output csv file.

        data (dict):
        Dictionary of salary statistics calculated in relation 
        to the company's department

    """
    if isinstance(output_file, str) is False:
        raise TypeError("Expected output file path as string")

    if isinstance(data, dict) is False:
        raise TypeError("Expected dictionary as second argument")

    if output_file.endswith((".csv")) is False:
        raise ValueError("Extension must be .csv")

    try:
        with open(output_file, 'w') as f:
            f.write(
                "dzial,srednia_wynagrodzen,mediana_wynagrodzen, dolne_widelki,gorne_widelki\n")
            for division, stats in data.items():
                f.write((f"{division}, {stats['mean']},"
                        f"{stats['median']},"
                         f"{stats['lower']},"
                         f"{stats['upper']}\n"))
    except KeyError as e:
        raise KeyError(f"Error: unexpected dictionary key: {e}")


if __name__ == "__main__":
    data = read_employee_data('.\src\data\sample_data.json')
    stats = get_salary_stats(data)
    save_data("output.csv", stats)
