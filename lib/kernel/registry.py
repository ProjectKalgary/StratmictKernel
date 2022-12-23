_register = []
_index = []

def set(name, value):
    if(_index.count(name) != 0):
        _register[_index.index(name)] = value
    else:
        _register.append(value)
        _index.append(name)

def get(name):
    return _register[_index.index(name)]
