from guard.usecase.bases import UseCase
from guard.usecase.suitus import UseCaseSuite
from guard.utils import generate_random_string


class UseCaseRegistry:

    def __init__(self) -> None:
        self._usecases = {}

    def register(self, usecase, name=None):
        if name is None:
            name = generate_random_string(20)
        if name not in self._usecases:
            self._usecases[name] = []

        self._usecases[name].append(usecase)

    def get_usecases(self):
        return [usecase for usecases in self._usecases.values() for usecase in usecases]


registry = UseCaseRegistry()


def register_suite(usecase_class):
    if not issubclass(usecase_class, UseCase):
        raise TypeError(f'{usecase_class} is not a subclass of `UseCase`.')

    usecase = usecase_class()

    if isinstance(usecase, UseCaseSuite):
        module = usecase.__module__
        for case in usecase.get_cases():
            registry.register(case, str(module))
