

ALLOWED_BULTINS = ['bool', 'dict', 'float', 'int', 'long', 'list', 'str', 'unicode']
ALLOWED_DATETIME = []


def process_mapping(data, map_options, root_path):
    root = getter(data, root_path)
    if isinstance(root, list):
        answer = [mapper(x, map_options) for x in root]
    else:
        answer = mapper(root, map_options)
    return answer

def mapper(data, fields_map):
    result = {}
    for key, map_rule in iter(fields_map.items()):
        datatype = map_rule.get('datatype')
        result[key] = getter(data, map_rule['path'])

        if datatype in ALLOWED_BULTINS:
            result[key] = getattr(__builtins__, datatype)(result[key])
        elif datatype == ALLOWED_DATETIME:
            result[key] = getattr(datetime, datatype)(result[key], **map_rule.get('options', {}))
    return result

def getter(data, path):
    source = data
    for node in path:
        if isinstance(node, str):
            source = source[node]
        elif isinstance(node, int):
            source = source[node]
        else:
            break
    return source
