from redis import Redis as _Redis    # non-std

class SRedis(_Redis):
    """Simple wrapper around confusingly pythonized Redis similar to later 'StrictRedis'"""
    def __init__(self, *v, **kw):
        _Redis.__init__(self, *v, **kw)

    def lpop(self, name):
        "Remove and return the first item of the list ``name``"
        return self.execute_command('LPOP', name)

    def lpush(self, name, *values):
        for value in values:
            self.push(name, value, head=True)
    def rpush(self, name, *values):
        for value in values:
            self.push(name, value, head=False)

    def rpop(self, name):
        return self.pop(name, tail=True)
    def lpop(self, name):
        return self.pop(name, tail=False)

