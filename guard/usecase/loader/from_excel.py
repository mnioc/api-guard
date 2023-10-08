import openpyxl
import json
from guard.usecase.loader.bases import UseCaseLoader
from collections import namedtuple
from guard.usecase.unit import UnitUseCase


UseCaseRow = namedtuple('UseCaseRow', ['name', 'method', 'url', 'headers', 'body', 'expect_status_code', 'expect_value'])


class ExcelUseCaseLoader(UseCaseLoader):

    exts = ['xlsx', 'xls']

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def read_excel(self):
        wb = openpyxl.load_workbook(self.file_path)
        ws = wb.active
        return [
            UseCaseRow(*row)
            for row in ws.iter_rows(min_row=2, values_only=True)
            if any(cell is not None for cell in row)
        ]

    def load(self, client) -> None:
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
                'json': json.loads(row.body),
                'assertions': self._get_assertions(row.expect_status_code, row.expect_value),
                'client': client
            }

            self.add_usecase(
                UnitUseCase(**kwargs)
            )
