from guard.usecase.loader.bases import UseCaseLoader
import importlib.util


class ModuleUseCaseLoader(UseCaseLoader):

    exts = ['py']

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def load(self, client) -> None:
        _name = self.file_path.split('/')[-1].split('.')[0]
        spec = importlib.util.spec_from_file_location(_name, self.file_path)
        module = importlib.util.module_from_spec(spec)
        _ = spec.loader.exec_module(module)
