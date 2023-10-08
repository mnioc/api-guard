from guard.usecase.unit import UnitUseCase
from guard.usecase.registry import registry
from guard.assertion.http import AssertHttpStatusCodeEqual, AssertHttpResponseValue


registry.register(
    UnitUseCase(
        name='createUser',
        method='POST',
        url='http://xxx.com/api/v1/user',
        headers={'Content-Type': 'application/json'},
        json={
            'username': 'test',
        },
        assertions=[
            AssertHttpStatusCodeEqual(200),
            AssertHttpResponseValue('$.code', 0)
        ]
    )
)
