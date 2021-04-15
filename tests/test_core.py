import unittest
import reports
from tablib import Dataset
from tempfile import gettempdir

tmp_folder = gettempdir()


class TestExecutor(unittest.TestCase):

    data = reports.Executor(Dataset(['Matteo', 'Guadrini', 35]))

    def test_executor_instance(self):
        self.assertIsInstance(self.data, reports.Executor)

    def test_get_data(self):
        self.assertIsInstance(self.data.get_data(), Dataset)
        self.assertEqual(str(self.data.get_data()), 'Matteo|Guadrini|35')

    def test_set_headers(self):
        self.data.headers(['name', 'surname', 'age'])
        self.assertEqual(self.data.data.headers, ['name', 'surname', 'age'])

    def test_filter_by_list(self):
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter([42])
        self.assertEqual(self.data.get_data()[0], ('Arthur', 'Dent', 42))
        self.data.reset()

    def test_filter_by_key(self):

        def is_answer(number):
            if number == 42:
                return True

        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter(key=is_answer)
        self.assertEqual(self.data.get_data()[0], ('Arthur', 'Dent', 42))
        self.assertEqual(self.data.get_data()[1], ('Ford', 'Prefect', 42))
        self.data.reset()

    def test_filter_by_list_and_column(self):
        self.data.headers(['name', 'surname', 'age'])
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter([42], column='age')
        self.assertEqual(self.data.get_data()[0], 42)
        self.data.reset()

    def test_map(self):

        def int_to_string(number):
            if isinstance(number, int):
                return str(number)
            else:
                return number

        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.map(int_to_string)
        self.assertEqual(self.data.get_data()[1], ('Arthur', 'Dent', '42'))
        self.assertEqual(self.data.get_data()[2], ('Ford', 'Prefect', '42'))
        self.data.reset()

    def test_select_column(self):
        self.data.headers(['name', 'surname', 'age'])
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        # By name
        self.assertEqual(self.data.select_column('age'), [35, 42, 42])
        # By number
        self.assertEqual(self.data.select_column(2), [35, 42, 42])
        self.data.reset()

    def test_count(self):
        self.assertEqual(len(self.data), 1)
        self.assertEqual(self.data.count_rows(), 1)
        self.data.headers(['name', 'surname', 'age'])
        self.assertEqual(self.data.count_column(), 3)

    def test_clone(self):
        new_data = self.data.clone()
        self.assertNotEqual(new_data, self.data)
        self.assertIsInstance(new_data, reports.Executor)
        self.assertEqual(type(new_data), type(self.data))


class TestReport(unittest.TestCase):

    input_data = Dataset(['Matteo', 'Guadrini', 35])
    output_data = reports.manager('csv', f'{tmp_folder}/test_csv.csv')
    title = 'Test report'
    filters = [42, 35]
    column = 'age'
    count = True
    report = reports.Report(input_data=input_data,
                            title=title,
                            filters=filters,
                            map_func=lambda item: str(item) if isinstance(item, int) else item,
                            column=column,
                            count=count,
                            output=output_data)

    def test_report_object(self):
        self.assertIsInstance(self.report, reports.Report)


if __name__ == '__main__':
    unittest.main()
