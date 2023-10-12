operator_map = {
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    'in': lambda x, y: x in y,
    'not in': lambda x, y: x not in y,
    'is': lambda x, y: x is y,
    'is not': lambda x, y: x is not y,
    'between': lambda x, y: y[0] <= x <= y[1],
    'contains': lambda x, y: y in x,
}

operator_range_map = {
    'all': lambda x, operator, _list: all(operator_map[operator](y, x) for y in _list),
    'any': lambda x, operator, _list: any(operator_map[operator](y, x) for y in _list),
}
