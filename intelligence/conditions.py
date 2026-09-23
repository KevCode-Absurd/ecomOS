"""Explicit AND/OR predicates with unknown facts preserved, never guessed.

Legacy equality dictionaries remain supported. Expressions use op plus either
args, arg, or fact/value. This interprets reviewed conditions, not model prose.
"""
import math


def scalar(value):
    return type(value) in {str, bool, int, float} and (
        type(value) is not float or math.isfinite(value))


def expression(condition):
    if not isinstance(condition, dict):
        raise ValueError('Condition must be an object')
    # "op" is reserved in expression objects. To compare a fact named "op",
    # use an explicit eq predicate instead of the legacy shorthand.
    if 'op' not in condition:
        if not all(isinstance(k, str) and k and scalar(v) for k, v in condition.items()):
            raise ValueError('Invalid equality conditions')
        return {'op': 'all', 'args': [{'op': 'eq', 'fact': k, 'value': v}
                                    for k, v in condition.items()]}
    return condition


def validate(condition, depth=0):
    if depth > 20:
        raise ValueError('Condition nesting exceeds limit')
    node = expression(condition)
    op = node.get('op')
    if not isinstance(op, str):
        raise ValueError('Invalid predicate operator')
    if op in {'all', 'any'}:
        if set(node) != {'op', 'args'} or not isinstance(node['args'], list):
            raise ValueError('Invalid logical predicate')
        if op == 'any' and not node['args']:
            raise ValueError('ANY needs at least one alternative')
        for arg in node['args']:
            validate(arg, depth + 1)
    elif op == 'not':
        if set(node) != {'op', 'arg'}:
            raise ValueError('Invalid NOT predicate')
        validate(node['arg'], depth + 1)
    elif op in {'eq', 'gte', 'lte'}:
        if set(node) != {'op', 'fact', 'value'} or not isinstance(node['fact'], str) or not node['fact'] or not scalar(node['value']):
            raise ValueError('Invalid comparison predicate')
        if op != 'eq' and type(node['value']) not in {int, float}:
            raise ValueError('Ranges require numerical values')
    else:
        raise ValueError('Unsupported condition operator')


def evaluate(condition, facts):
    """Return True, False or None (unknown). Validate before evaluation."""
    validate(condition)

    def visit(raw):
        node = expression(raw)
        op = node['op']
        if op in {'all', 'any'}:
            results = [visit(arg) for arg in node['args']]
            if op == 'all':
                return False if False in results else None if None in results else True
            return True if True in results else None if None in results else False
        if op == 'not':
            result = visit(node['arg'])
            return None if result is None else not result
        value = facts.get(node['fact'])
        if node['fact'] not in facts or not scalar(value):
            return None
        expected = node['value']
        if op == 'eq':
            return type(value) is type(expected) and value == expected
        if type(value) not in {int, float}:
            return None
        return value >= expected if op == 'gte' else value <= expected

    return visit(condition)


def excluded(condition, facts):
    """Legacy exclusion mappings mean ANY match; expression logic is explicit."""
    node = expression(condition)
    if node is not condition:
        if not node['args']:
            return False
        node['op'] = 'any'
    return evaluate(node, facts)
