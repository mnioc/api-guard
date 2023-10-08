import yaml
from guard.usecase.loader.bases import UseCaseLoader
from guard.usecase.unit import UnitUseCase


class YamlUseCaseLoader(UseCaseLoader):

    exts = ['yaml', 'yam']

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def read_yaml(self):
        with open(self.file_path, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def load(self, client) -> None:
        """
        This method is used to load use case from excel file.
        """
        data = self.read_yaml()
        for item in data:
            kwargs = {
                'name': item.get('name'),
                'method': item.get('method'),
                'url': item.get('url'),
                'headers': item.get('headers'),
                'json': item.get('body'),
                'client': client,
                'assertions': self._get_assertions(item.get('expect_status_code'), item.get('expect_value'))
            }

            self.add_usecase(
                UnitUseCase(**kwargs)
            )
