import argparse
import csv
from tabulate import tabulate


def load_data(file_path):
    """Загружаем данные из CSV."""
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def apply_filter(data, filter_expr):
    """
    Применяет фильтр к данным согласно заданному выражению.

    Формат выражения: <column><оператор><value>,
                     где оператор может быть '=', '>', '<'.

    Например: "price>500", "brand=Acer"
    """
    parts = filter_expr.split(None, 1)  # Разделение по первому пробелу, чтобы выделить колонку и выражение вместе
    if len(parts) != 2:
        raise ValueError("Некорректный формат фильтра. Используйте format: column<оператор>value")

    column, expr = parts
    operator = None
    value = None

    # Анализируем выражение
    if '=' in expr:
        operator = '='
        value = expr.strip('= ')
    elif '>' in expr:
        operator = '>'
        value = expr.strip('> ')
    elif '<' in expr:
        operator = '<'
        value = expr.strip('< ')
    else:
        raise ValueError("Оператор отсутствует или неверный. Допустимы только '=', '>', '<'.")

    filtered_data = []
    for row in data:
        current_value = row[column]
        # Преобразуем в число, если возможно
        try:
            current_value = float(current_value)
            value = float(value)
        except ValueError:
            pass  # Оставляем как строку, если преобразовать нельзя

        # Логика проверки условия
        if ((operator == '=' and current_value == value) or
            (operator == '>' and current_value > value) or
            (operator == '<' and current_value < value)):
            filtered_data.append(row)

    return filtered_data


def aggregate_values(filtered_data, column, agg_func):

    """
    Выполняет агрегацию над столбцом чисел (среднее, минимальное, максимальное).
    Возможные агрегатные функции: min, max, avg.
    """
    values = [float(row[column]) for row in filtered_data]
    if len(values) == 0:
        raise ValueError("Нет данных для агрегирования.")

    if agg_func == 'min':
        result = min(values)
    elif agg_func == 'max':
        result = max(values)
    elif agg_func == 'avg':
        result = sum(values) / len(values)
    else:
        raise ValueError(f'Неверное имя агрегатной функции "{agg_func}"')

    return {f"{agg_func}({column})": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обрабатываем CSV файл")
    parser.add_argument("--file", required=True, help="Путь к файлу CSV")
    parser.add_argument("--filter", help="Фильтр формата column=<|>|==value")
    parser.add_argument('--aggregate', nargs=2, metavar=('field', 'op'),
                        help='Операция агрегации (field op): field - название колонки, '
                             'op - одна из операций: max, min, avg.')

    args = parser.parse_args()
    # Загрузка данных
    data = load_data(args.file)

    # Применяем фильтры, если указаны
    if args.filter:
        data = apply_filter(data, args.filter)

    # Проводим агрегацию, если указана
    aggregated_result = None
    if args.aggregate:
        column_to_aggregate, agg_function = args.aggregate
        aggregated_result = aggregate_values(data, column_to_aggregate, agg_function)

    # Печатаем результат в виде таблицы
    rows = data
    print(tabulate(rows, headers='keys'))
    if args.aggregate:
        print(tabulate([aggregated_result], headers='keys'))