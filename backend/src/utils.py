import json


def stream_json(records):
    yield "["
    first = True
    for row in records:
        if not first:
            yield ","
        else:
            first = False
        yield json.dumps(dict(row))
    yield "]"
