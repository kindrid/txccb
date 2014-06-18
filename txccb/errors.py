

class CCBError(Exception):

    def __init__(self, message, number=None, type_=None):
        args = [number, type_]
        self.number = number
        self.type_ = type_
        Exception.__init__(self, message, *args)
