from guard.usecase.bases import UseCase
from guard.usecase.suitus import UseCaseSuite


class UseCaseRegistry:

    def __init__(self) -> None:
        self._usecases = []

    def register(self, usecase):
        self._usecases.append(usecase)

    def get_usecases(self):
        return self._usecases


registry = UseCaseRegistry()


def register_suite(usecase_class):
    if not issubclass(usecase_class, UseCase):
        raise TypeError(f'{usecase_class} is not a subclass of `UseCase`.')

    usecase = usecase_class()

    if isinstance(usecase, UseCaseSuite):
        for case in usecase.get_cases():
            registry.register(case)
