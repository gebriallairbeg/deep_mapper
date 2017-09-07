import re
from contextlib import suppress


def process_mapping(data, map_options, root_path):
    '''
    central block that will find the obj-root from which will starts the mapping
    and then perform mapping for each objects (or one) starting from this root

    params:
        data: py-object that need to be conversed

        map_options: dict-based map structure that helps to establish the
        relationship of keys and types

        root_path: xpath-like sting which indicates to the root of all path-es in map_options
        especially needed when the result of the function must be a list
    '''

    # TODO: temporal solution to support clear XPath syntax
    # will be re-written wtih as new getter using some external solution
    for key in map_options:
        map_options[key]['path'] = normalize_path(map_options[key]['path'])
    root_path = normalize_path(root_path or '')

    root = getter(data, root_path)
    if isinstance(root, list):
        answer = [mapper(x, map_options) for x in root]
    else:
        answer = mapper(root, map_options)
    return answer

def mapper(data, fields_map):
    '''
    actually a mapper function that will process each node with prepeared rules from fields_map
    '''
    result = {}
    for key, map_rule in iter(fields_map.items()):
        postprocess = map_rule.get('postprocess')
        result[key] = getter(data, map_rule['path'])

        if postprocess is not None:
            with suppress(Exception):
                result[key] = postprocess(result[key], *map_rule.get('args', []), **map_rule.get('kwargs', {}))
    return result

def normalize_path(path_as_str):
    '''
    just transforms xpath-like string to array that could be processed with getter
    '''
    path_as_str = re.sub(r'(?P<idx>\[\d+\])', r'/\g<idx>', path_as_str)
    path = [int(node[1:-1]) if re.search(r'\[\d+\]', node) else node
            for node in path_as_str.strip('/').split('/')]
    return path

def getter(data, path):
    '''
    catches each node based on array stored xpath items
    xpath key-rules, that supported right now:
    /key        - node`s child access
    /key[idx]   - array`s item access
    '''
    source = data
    for node in path:
        if isinstance(node, str) and isinstance(source, dict):
            source = source.get(node)
        elif isinstance(node, int) and isinstance(source, list):
            source = source[node] if len(source) > node else None
        else:
            break
    return source
