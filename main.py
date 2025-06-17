import argparse
import csv
from tabulate import tabulate


def load_data(file_path: str) -> list:
    """Загружаем данные из CSV."""
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def apply_filter(data: list, filter_expr: str) ->list:

    parts = filter_expr.split(None, 1)
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
        try:
            current_value = float(current_value)
            value = float(value)
        except ValueError:
            pass

        if ((operator == '=' and current_value == value) or
            (operator == '>' and current_value > value) or
            (operator == '<' and current_value < value)):
            filtered_data.append(row)

    return filtered_data

def order(data: list, filter_expr: str) ->list:

    parts = filter_expr.split("=")
    if len(parts) != 2:
        raise ValueError("Некорректный формат. Используйте format: column=value")
    column, expr = parts

    filtered_data = []
    for row in data:
        try:
            current_value = row[column]
            filtered_data.append(float(current_value))
        except Exception as exp:
            raise ValueError(f"Ошибка. Поле {column} не является int или float")
    if expr == 'asc':
        filtered_data = sorted(filtered_data, reverse=True)
    elif expr == 'desc':
        filtered_data = sorted(filtered_data, reverse=False)
    return [row for i in filtered_data for row in data if float(row[column]) == i]


def aggregate_values(filtered_data: list, column: str, agg_func: str)-> dict:
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
    parser.add_argument("--filter", help="Фильтр формата column<оператор>value")
    parser.add_argument('--aggregate', nargs=2, metavar=('field', 'op'),
                        help='Операция агрегации (field op): field - название колонки, '
                             'op - одна из операций: max, min, avg.')
    parser.add_argument("--order-by",  help="Формат column=value")

    args = parser.parse_args()

    data = load_data(args.file)

    # Применяем фильтры, если указаны
    if args.filter:
        data = apply_filter(data, args.filter)
    if args.order_by:
        data = order(data, args.order_by)


    aggregated_result = None
    if args.aggregate:
        column_to_aggregate, agg_function = args.aggregate
        aggregated_result = aggregate_values(data, column_to_aggregate, agg_function)

    rows = data if not aggregated_result else [aggregated_result]
    print(tabulate(rows, headers='keys'))