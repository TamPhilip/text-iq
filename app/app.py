from flask import Flask, request
import json
import inspect

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj

class ItemObject(object):
    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {"name": self.name}


app = Flask(__name__)
items = []
id = 0

@app.route('/', methods=['GET'])
def get():
    return json.dumps({"items" : items},cls=ObjectEncoder, indent=2)


@app.route('/create/', methods=['PUT', 'POST'])
def create():
    """
        Creates the item with the correct name items json
        If not found returns items json
        @:item name query request
        :return:
        """
    name = request.args.get('item')
    item = ItemObject(name)
    items.append(item)
    return json.dumps({"items" : items}, cls=ObjectEncoder, indent=2)

@app.route('/delete/', methods=['GET', 'DELETE'])
def delete():
    """
    Finds the first item in items and deletes it and returns items json
    If not found returns items json
    @:item name query request
    :return:
    """
    name = request.args.get('item')
    for item in items:
        if(item.name == name):
            items.remove(item)
            break
    return json.dumps({"items": items}, cls=ObjectEncoder, indent=2)

if __name__ == '__main__':
    app.run()
