import inspect
from typing import List, Optional, Union, Callable, Dict, Any
from colorama import Fore
from prettytable import PrettyTable
import json
from guard.usecase.unit import UnitUseCase
from guard.usecase.bases import UseCase


class UseCaseSuite(UseCase):

    show_result = False
    show_response_body = False

    def __init__(
        self,
        cases: Optional[List[UnitUseCase]] = None,
        pre_hooks: Optional[List[dict]] = None,
        post_hooks: Optional[List[dict]] = None,
    ):
        self._cases = cases or []
        self.pre_hooks = pre_hooks or []
        self.post_hooks = post_hooks or []
        super().__init__()

    def get_cases(self) -> List[UnitUseCase]:
        return self._cases

    def add_case(self, case: UseCase) -> None:
        assert isinstance(case, UseCase), '`case` must be `UseCase`'
        self._cases.append(case)

    def add_cases(self, cases: List[UnitUseCase]) -> None:
        for case in cases:
            self.add_case(case)

    def show(self):
        for case in self._cases:
            body = json.dumps(case.request.json)
            if case.passed:
                print(Fore.GREEN+'-' * 150)
                print(f'case_name | {Fore.GREEN}{case.name}')
                print(f'status    | {Fore.GREEN}PASSED')
                if case.request.json:
                    print(f'body      | {Fore.GREEN}{body}')
                if self.show_response_body:
                    try:
                        print(f'response  | {Fore.GREEN}{case.response.json()}')
                    except Exception:
                        print(f'response  | {Fore.GREEN}{case.response.text}')
            else:
                print(Fore.RED+'-' * 150)
                print(f'case_name | {Fore.RED}{case.name}')
                print(f'status    | {Fore.RED}FAILURE')
                if case.request.json:
                    print(f'body      | {Fore.RED}{body}')
                reason = ''.join(f'<{point.error_message}>' for point in case.failed_check_points)
                print(f'reason    | {Fore.RED}{reason}')
                if self.show_response_body:
                    try:
                        print(f'response  | {Fore.RED}{case.response.json()}')
                    except Exception:
                        print(f'response  | {Fore.RED}{case.response.text}')

    def execute(self, client=None) -> None:
        self.execute_pre_hooks()
        for test_case in self._cases:
            test_case.execute(client)

        if self.show_result:
            self.show()
        self.execute_post_hooks()
