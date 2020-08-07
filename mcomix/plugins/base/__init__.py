

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class BasePlugin(object):
    @classproperty
    def name(self):
        return self.__name__


class ArchiveReader(BasePlugin):
    pass
