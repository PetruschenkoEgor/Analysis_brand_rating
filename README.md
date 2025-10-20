## Запуск программы командами:
- Вывод всего содержимого:
python -m main --file products1.csv
- Вывод отчета по одному файлу:
python -m main --file products1.csv --report average-rating
- Вывод отчета по нескольким файлам:
python -m main --file products1.csv,products2.csv --report average-rating

## Запуск тестов:
- Запуск тестов загрузки csv файлов:
python -m pytest tests/test_csv_data.py -v
- Запуск тестов создания отчета по рейтингам брендов:
python -m pytest tests/test_average_rating.py -v
- Проверка покрытия тестами:
pytest --cov=.
