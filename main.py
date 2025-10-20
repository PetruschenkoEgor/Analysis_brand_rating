import argparse

from tabulate import tabulate

from commands.average_rating_command import AverageRatingCommand
from models.csv_data import CSVData


def main():
    parser = argparse.ArgumentParser(description="Process CSV file")
    parser.add_argument("--file", help="Путь до CSV файла")
    parser.add_argument("--report", nargs="?", const="default", help="Отчет по среднему рейтингу бренда")

    args = parser.parse_args()

    if not args.file:
        print("Необходимо указать --file")
        return

    # Загрузка данных
    csv_data = CSVData.load_from_many_files(args.file)

    # Применение команды создания отчета, если указано
    if args.report:
        report = AverageRatingCommand()
        report.get_rating(csv_data.rows)
        result = report.execute()
        print(tabulate(result, headers="keys", tablefmt="grid"))
    else:
        print(tabulate(csv_data.rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
