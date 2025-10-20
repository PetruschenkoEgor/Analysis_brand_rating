import csv
from typing import Any, Dict, List


class CSVData:
    """Класс для загрузки и хранения данных CSV."""

    def __init__(self, rows: List[Dict[str, Any]]):
        self.rows = rows

    @staticmethod
    def load_from_file(file_path: str) -> "CSVData":
        """Загружает данные из CSV-файла и возвращает экземпляр CSVData."""

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Конвертируем числа из строк
        rows = CSVData._convert_numeric_values(rows)
        return CSVData(rows)

    @staticmethod
    def load_from_many_files(files: str) -> "CSVData":
        """Загружает данные из нескольких CSV-файлов и возвращает экземпляр CSVData."""

        result = []
        if files:
            list_file = files.split(",")
            for file in list_file:
                file_csv_data = CSVData.load_from_file(file.strip())
                result.extend(file_csv_data.rows)
        return CSVData(result)

    @staticmethod
    def _convert_numeric_values(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Пытается преобразовать строки в числа, если это возможно."""

        for row in rows:
            for key, value in row.items():
                if isinstance(value, str):
                    if value.isdigit():
                        row[key] = int(value)
                    elif value.replace(".", "", 1).isdigit() and value.count(".") == 1:  # Проверяем на float
                        row[key] = float(value)
        return rows
