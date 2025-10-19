from typing import Any, List, Dict
from numpy import mean
from commands.base_command import BaseCommand


class AverageRatingCommand(BaseCommand):
    """Команда для формирования отчета. Отчёт включает в себя список брендов и средний рейтинг бренда, бренды сортируются по рейтингу."""

    def __init__(self):
        self.brands = {}
        self.report = []

    def get_rating(self, data:  List[Dict[str, Any]]) -> None:
        """Получаем все рейтинги по брендам."""
        for row in data:
            try:
                brand = row.get("brand")
                rating = row.get("rating")

                # Проверяем, что brand и rating существуют
                if brand and rating is not None:
                    if brand not in self.brands:
                        self.brands[brand] = []
                    self.brands[brand].append(float(rating))
            except (ValueError, TypeError) as e:
                print(f"Ошибка: {e}")
                continue

    def execute(self) -> list[Any]:
        """Вычисляем данные для отчета."""
        for brand, ratings in self.brands.items():
            try:
                if ratings:
                    # Получаем средний рейтинг
                    avg_rating = mean(ratings)
                    dict_report = dict(brand=brand, rating=round(avg_rating, 2))
                    self.report.append(dict_report)
            except Exception as e:
                print(f"Ошибка: {e}")
                continue
        self.report.sort(key=lambda x: x['rating'], reverse=True)
        return self.report
