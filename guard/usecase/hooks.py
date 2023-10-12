from guard.logger import logger
from guard.utils import get_value_from_json_path
from guard.http.hooks import show_response_table


def show_usecase_table(usecase, *args, **kwargs) -> None:
    """
    This function is used to show the use case in a table format.
    """
    response = usecase.response
    show_response_table(response, *args, **kwargs)


def setup_data(
    usecase,
    client,
    get_pk_json_path,
    url_template,
    request_kwargs=None,
    auto_clean_up=True,
    set_usecase_url=True,
):
    """
    This function is used to set the use case url from pk.
    """
    from guard.usecase.unit import UnitUseCase
    from guard.usecase.suitus import UseCaseSuite

    res = client.request(**(request_kwargs or {}))

    try:
        res_data = res.json()
    except Exception as e:
        raise e
    pk = get_value_from_json_path(res_data, get_pk_json_path)
    url = url_template

    if pk is None:
        logger.warning(f'pk is None, {res_data}')
    if pk is not None and r'{pk}' in url_template:
        url = url_template.format(pk=pk)

    if isinstance(usecase, UnitUseCase) and set_usecase_url:
        usecase.set_request_url(url)

    elif isinstance(usecase, UseCaseSuite):
        for case in usecase.get_cases():
            if set_usecase_url:
                case.set_request_url(url)

    if auto_clean_up:
        usecase.add_post_hook(
            {
                'func': client.delete,
                'kwargs': {
                    'url': url,
                },
            }
        )


def clean_up(
    usecase,
    client,
    get_pk_json_path,
    url_template,
):
    from guard.usecase.unit import UnitUseCase
    from guard.usecase.suitus import UseCaseSuite

    if isinstance(usecase, UnitUseCase):
        unit_usecase_clean_up(usecase, client, get_pk_json_path, url_template)
    elif isinstance(usecase, UseCaseSuite):
        for case in usecase.get_cases():
            if _ := unit_usecase_clean_up(
                case, client, get_pk_json_path, url_template
            ):
                return


def unit_usecase_clean_up(usecase, client, get_pk_json_path, url_template):
    response = usecase.response
    try:
        res_data = response.json()
    except Exception as e:
        raise e
    pk = get_value_from_json_path(res_data, get_pk_json_path)
    url = None
    if pk is not None and r'{pk}' in url_template:
        url = url_template.format(pk=pk)

    logger.info(f'clean up {url}')
    res = client.delete(url=url)
    if res.status_code == 204:
        return True


def string_to_datetime(
    date_string: str,
    format: str = '%Y-%m-%d %H:%M:%S',
    pytz_timezone: str = 'Asia/Shanghai',
):
    """
    This function is used to convert string to datetime.
    """
    from datetime import datetime
    import pytz

    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, format).astimezone(pytz.timezone(pytz_timezone))
    except Exception as e:
        raise e
