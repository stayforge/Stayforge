class ModelNotFoundError(ValueError):
    """ 在Source中找不到插件 """

    def __init__(self, *args, **kwargs):
        pass

class ModelNameError(ValueError):
    """ Invalid Name format (only A-Za-z and -) """

    def __init__(self, *args, **kwargs):
        pass

class ModelPathError(ValueError):
    """ Invalid Path format. must be `namespace/name or name` """

    def __init__(self, *args, **kwargs):
        pass
