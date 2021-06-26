import json

registered_transformation = {
    'int': lambda x: int(x),
    'str': lambda x: str(x),
    'float': lambda x: float(x),
    'list': lambda x: list(x),
    'json': lambda x: json.dumps(x),
    'json_dict': lambda x: json.loads(x),
}
