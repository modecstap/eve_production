from src.services.exceptions import ServiceException


class ProductCountException(ServiceException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'ProductCountException, {self.message}'
        else:
            return 'ProductCountException: the number of required products exceeds the available ones'
