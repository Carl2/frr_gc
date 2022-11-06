class Error:
    def __init__(self, error_msg):
        "docstring"
        self.error_msg = error_msg


class Monad:
    def __init__(self, args):

        #self.is_value = False
        self.value = args


    @property
    def is_value(self):
        return self._is_value

    @is_value.setter
    def is_value(self,val):
        self._is_value = val



    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):

        self.is_value = type(val) is not Error
        self._value = val


def transform( fn):
    def execute_transform(arg):

        if arg.is_value:
            return fn(arg.value)
        else:
            return arg

    return execute_transform
