import openpyxl
from guard.usecase.loader.bases import UseCaseLoader
from collections import namedtuple
from guard.usecase.unit import UnitUseCase


UseCaseRow = namedtuple('UseCaseRow', ['name', 'method', 'url', 'headers', 'body', 'expect_status_code', 'expect_value'])


class ExcelUseCaseLoader(UseCaseLoader):

    exts = ['xlsx', 'xls']

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path
        self.read_excel()

    def read_excel(self):
        wb = openpyxl.load_workbook(self.file_path)
        ws = wb.active
        return [UseCaseRow(*row) for row in ws.iter_rows(min_row=2, values_only=True)]

    def load(self) -> None:
        """
        This method is used to load use case from excel file.
        """
        rows = self.read_excel()
        for row in rows:
            kwargs = {
                'name': row.name,
                'method': row.method,
                'url': row.url,
                'headers': row.headers,
                'json': row.body,
                'assertions': self._get_assertions(row.expect_status_code, row.expect_value)
            }

            self.add_usecase(
                UnitUseCase(**kwargs)
            )


if __name__ == '__main__':
    loader = ExcelUseCaseLoader('/home/bot/mnio/api-guard/examples/excel/test_user.xlsx')
    loader.load()
    print(loader.usecases)