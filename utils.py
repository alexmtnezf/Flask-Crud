def logger(func):
    """
    Decorator for logging parameters in a function call
    :param func: Function to decorate
    :return: Decorated function
    """

    def inner(*args, **kwargs):
        print("Arguments were: %s, %s" % (args, kwargs))
        return func(*args, **kwargs)

    return inner
