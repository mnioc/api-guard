import inspect
from typing import Dict, List, Optional, Union, Callable
from guard.logger import logger



class UseCase:

    _name = None

    def __init__(
        self,
        name: str = None,
        pre_hooks: Optional[List[dict]] = None,
        post_hooks: Optional[List[dict]] = None,
    ):
        self.name = name or self._name
        self.passed = True
        self.failed_reason = []
        self.pre_hooks = pre_hooks or []
        self.post_hooks = post_hooks or []

    def add_pre_hook(self, hook: dict) -> None:
        """
        This method is used to add a pre hook.
        """
        """
        This method is used to add a post hook.
        """
        if isinstance(hook, dict):
            if hook not in self.pre_hooks:
                self.pre_hooks.append(hook)
        else:
            self.add_pre_hook({'func': hook})

    def clear_pre_hooks(self) -> None:
        """
        This method is used to clear pre hooks.
        """
        self.pre_hooks = []

    def extend_pre_hooks(self, hooks: list) -> None:
        """
        This method is used to extend pre hooks.
        """
        for hook in hooks:
            self.add_pre_hook(hook)

    def add_post_hook(self, hook: Union[Dict, Callable]) -> None:
        """
        This method is used to add a post hook.
        """
        if isinstance(hook, dict):
            if hook not in self.post_hooks:
                self.post_hooks.append(hook)
        else:
            self.add_post_hook({'func': hook})

    def clear_post_hooks(self) -> None:
        """
        This method is used to clear post hooks.
        """
        self.post_hooks = []

    def extend_post_hooks(self, hooks: list) -> None:
        """
        This method is used to extend post hooks.
        """
        for hook in hooks:
            self.add_post_hook(hook)

    def do_fail(self):
        self.passed = False

    def add_failed_reason(self, reason: str):
        self.failed_reason.append(reason)

    def execute_hooks(self, hooks):
        """
        This method is used to execute hooks.
        """
        for hook in hooks:
            func = hook.get('func')
            if func is not None and callable(func):
                func_signature = inspect.signature(func)
                func_params = func_signature.parameters.keys()
                if 'usecase' in func_params:
                    func(usecase=self, *hook.get('args', []), **hook.get('kwargs', {}))
                else:
                    func(*hook.get('args', []), **hook.get('kwargs', {}))

    def execute_post_hooks(self) -> None:
        """
        This method is used to execute post hooks.
        """
        self.execute_hooks(self.post_hooks)

    def execute_pre_hooks(self) -> None:
        """
        This method is used to execute pre hooks.
        """
        self.execute_hooks(self.pre_hooks)

    def execute(self, *args, **kwargs):
        raise NotImplementedError
