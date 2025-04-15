from src.services.exceptions import ServiceException


class NotEnoughMaterialsException(ServiceException):
    def __init__(self, missing_materials: dict, *args):
        if args:
            self.missing_materials: dict = missing_materials
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return (f'NotEnoughMaterialsException, There are not enough materials to create the requested products '
                    f'missing: {self.missing_materials}')
        else:
            return 'NotEnoughMaterialsException: There are not enough materials to create the requested products'
