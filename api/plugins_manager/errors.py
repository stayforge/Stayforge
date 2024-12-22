class PluginNotFoundError(ValueError):
    """ 在Source中找不到插件 """

    def __init__(self, *args, **kwargs):
        pass

class PluginNameError(ValueError):
    """ Invalid Name format (only A-Za-z and -) """

    def __init__(self, *args, **kwargs):
        pass

class PluginPathError(ValueError):
    """ Invalid Path format. must be `namespace/name or name` """

    def __init__(self, *args, **kwargs):
        pass
