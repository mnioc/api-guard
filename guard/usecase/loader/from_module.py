from guard.usecase.loader.bases import UseCaseLoader
import importlib.util
from guard.usecase.unit import UnitUseCase


class ModuleUseCaseLoader(UseCaseLoader):

    exts = ['py']

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def load(self, client) -> None:
        """
        This method is used to load use case from excel file.
        """
        spec = importlib.util.spec_from_file_location('client', self.file_path)
        module = importlib.util.module_from_spec(spec)
        _ = spec.loader.exec_module(module)

        for var_name in dir(module):
            if isinstance(usecase := getattr(module, var_name), UnitUseCase):
                if usecase.client is None:
                    usecase.client = client
                self.add_usecase(usecase)
