

class UseCase:

    _name = None

    def __init__(self, name: str = None):
        self.name = name or self._name
        self.passed = True
        self.failed_reason = []

    def do_fail(self):
        self.passed = False

    def add_failed_reason(self, reason: str):
        self.failed_reason.append(reason)

    def execute(self, *args, **kwargs):
        raise NotImplementedError
