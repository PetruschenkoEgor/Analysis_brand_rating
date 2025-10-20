import pytest

from commands.average_rating_command import AverageRatingCommand


class TestAverageRatingCommand:
    """Тесты для класса AverageRatingCommand."""

    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными."""
        return [
            {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
            {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8},
            {"name": "redmi note 12", "brand": "xiaomi", "price": 199, "rating": 4.6},
            {"name": "iphone 14", "brand": "apple", "price": 799, "rating": 4.7},
            {"name": "galaxy a54", "brand": "samsung", "price": 349, "rating": 4.2},
        ]

    @pytest.fixture
    def command_with_data(self, sample_data):
        """Фикстура с командой и загруженными данными."""
        command = AverageRatingCommand()
        command.get_rating(sample_data)
        return command

    def test_get_rating_brand_collection(self, command_with_data):
        """Тест корректного сбора рейтингов по брендам."""
        expected_brands = {"apple": [4.9, 4.7], "samsung": [4.8, 4.2], "xiaomi": [4.6]}
        assert command_with_data.brands == expected_brands

    def test_execute_sorting(self, command_with_data):
        """Тест сортировки по рейтингу (по убыванию)."""
        result = command_with_data.execute()

        # Проверяем сортировку
        ratings = [item["rating"] for item in result]
        assert ratings == sorted(ratings, reverse=True)

        assert result[0]["rating"] == pytest.approx(4.8)  # apple
        assert result[1]["rating"] == pytest.approx(4.6)  # xiaomi
        assert result[2]["rating"] == pytest.approx(4.5)  # samsung

    def test_empty_data(self):
        """Тест с пустыми данными."""
        command = AverageRatingCommand()
        command.get_rating([])
        result = command.execute()
        assert result == []

    def test_missing_brand_field(self):
        """Тест с данными без поля brand."""
        data = [
            {"name": "iphone 15 pro", "rating": 4.9},
            {"name": "galaxy s23 ultra", "brand": "samsung", "rating": 4.8},
        ]
        command = AverageRatingCommand()
        command.get_rating(data)
        result = command.execute()

        # Должен быть только один бренд
        assert len(result) == 1
        assert result[0]["brand"] == "samsung"

    def test_missing_rating_field(self):
        """Тест с данными без поля rating."""
        data = [{"brand": "apple", "rating": 4.5}, {"brand": "samsung"}]
        command = AverageRatingCommand()
        command.get_rating(data)
        result = command.execute()

        # Должен быть только один бренд с рейтингом
        assert len(result) == 1
        assert result[0]["brand"] == "apple"

    def test_invalid_rating_values(self):
        """Тест с некорректными значениями рейтинга."""
        data = [
            {"brand": "apple", "rating": "4.5"},
            {"brand": "samsung", "rating": "invalid"},
            {"brand": "xiaomi", "rating": None},
        ]
        command = AverageRatingCommand()
        command.get_rating(data)
        result = command.execute()

        # Должен быть только один бренд
        assert len(result) == 1
        assert result[0]["brand"] == "apple"
