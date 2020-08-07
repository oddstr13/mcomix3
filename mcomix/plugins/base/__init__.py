

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class BasePlugin(object):
    @classproperty
    def name(self):
        return self.__name__


class TestingDummyPlugin(BasePlugin):
    """
    This is a dummy class for testing plugin loading.
    DO NOT USE!
    """
    pass
