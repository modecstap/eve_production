from src.services.exceptions import ServiceException


class NotEnoughMaterialsException(ServiceException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'NotEnoughMaterialsException, {self.message}'
        else:
            return 'NotEnoughMaterialsException: There are not enough materials to create the requested products'
