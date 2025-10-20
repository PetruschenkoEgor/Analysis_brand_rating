import pytest
import tempfile
import os
from models.csv_data import CSVData


class TestCSVData:
    """Тесты для класса CSVData."""

    def test_load_from_file(self):
        """Тест загрузки данных из CSV файла."""
        # Создаем временный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("name,brand,price,rating\niphone 15 pro,apple,999,4.9\ngalaxy s23 ultra,samsung,1199,4.8\n")
            temp_path = f.name

        try:
            csv_data = CSVData.load_from_file(temp_path)

            assert isinstance(csv_data, CSVData)
            assert len(csv_data.rows) == 2
            assert csv_data.rows[0] == {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9}
            assert csv_data.rows[1] == {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8}

        finally:
            # Удаляем временный файл
            os.unlink(temp_path)

    def test_load_from_file_numeric_conversion(self):
        """Тест конвертации чисел."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("price,rating\n100,4.5\n200,4.8\n")
            temp_path = f.name

        try:
            csv_data = CSVData.load_from_file(temp_path)

            assert isinstance(csv_data.rows[0]['price'], int)
            assert isinstance(csv_data.rows[0]['rating'], float)

        finally:
            os.unlink(temp_path)

    def test_load_from_many_files(self):
        """Тест загрузки из нескольких файлов."""
        files = []
        try:
            # Первый файл
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
                f.write("name,brand,price,rating\niphone 15 pro,apple,999,4.9\ngalaxy s23 ultra,samsung,1199,4.8\n")
                files.append(f.name)

            # Второй файл
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
                f.write(
                    "name,brand,price,rating\nredmi note 12,xiaomi,199,4.6\niphone 14,apple,799,4.7\ngalaxy a54,samsung,349,4.2\n")
                files.append(f.name)

            # Загружаем файлы
            file_paths = ",".join(files)
            csv_data = CSVData.load_from_many_files(file_paths)

            assert isinstance(csv_data, CSVData)
            assert len(csv_data.rows) == 5

        finally:
            for file_path in files:
                os.unlink(file_path)

    def test_load_from_many_files_empty(self):
        """Тест загрузки без файлов."""
        csv_data = CSVData.load_from_many_files("")
        assert isinstance(csv_data, CSVData)
        assert len(csv_data.rows) == 0

    def test_file_not_found(self):
        """Тест ошибки при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            CSVData.load_from_file("nonexistent_file.csv")
