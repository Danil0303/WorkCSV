import io
import unittest
from main import load_data, apply_filter, aggregate_values, order


class TestCsvProcessor(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {'product_id': '1', 'brand': 'Acer', 'price': '499'},
            {'product_id': '2', 'brand': 'Dell', 'price': '799'},
            {'product_id': '3', 'brand': 'Huawei', 'price': '1299'},
            {'product_id': '4', 'brand': 'MacBook', 'price': '1499'}
        ]

    def test_load_data(self):
        """Тест загрузки данных из CSV."""
        # Имитация открытия файла с данными
        fake_file_content = "\n".join([
            "product_id,brand,price",
            "1,Acer,499",
            "2,Dell,799",
            "3,Huawei,1299",
            "4,MacBook,1499"
        ])
        mock_file = io.StringIO(fake_file_content)
        # Подменяем открытый файл нашим объектом StringIO
        from unittest.mock import patch
        with patch('builtins.open', return_value=mock_file):
            loaded_data = load_data("fake/path/to/file.csv")
            self.assertEqual(len(loaded_data), 4)
            self.assertIn({'product_id': '1', 'brand': 'Acer', 'price': '499'}, loaded_data)

    def test_apply_filter_equality(self):
        filtered_data = apply_filter(self.test_data, "brand = Acer")
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['brand'], 'Acer')

    def test_apply_filter_greater_than(self):
        filtered_data = apply_filter(self.test_data, "price > 1000")
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue(all(float(d['price']) > 1000 for d in filtered_data))

    def test_apply_filter_less_than(self):
        filtered_data = apply_filter(self.test_data, "price < 500")
        self.assertEqual(len(filtered_data), 1)
        self.assertTrue(all(float(d['price']) < 500 for d in filtered_data))

    def test_aggregate_min(self):
        result = aggregate_values(self.test_data, "price", "min")
        self.assertDictEqual(result, {"min(price)": 499})

    def test_aggregate_max(self):
        result = aggregate_values(self.test_data, "price", "max")
        self.assertDictEqual(result, {"max(price)": 1499})

    def test_empty_aggregation(self):
        with self.assertRaises(ValueError):
            aggregate_values([], "price", "min")



