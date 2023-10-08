
class UseCaseRegistry:

    def __init__(self) -> None:
        self._usecases = []

    def register(self, usecase):
        self._usecases.append(usecase)

    def get_usecases(self):
        return self._usecases


registry = UseCaseRegistry()
