import argparse
import os
import re

import yaml

from src.config.config import Config
from src.extensions import Singleton


class Settings(metaclass=Singleton):
    def __init__(self):
        parser = argparse.ArgumentParser(description="Описание вашего приложения")
        parser.add_argument('--env', type=str, help='Выбор значения окружения')

        args = parser.parse_args()

        # тут в будущем настроить выбор файла в зависимости от env
        if args.env in ['dev', 'prod']:
            filename = 'config.yaml'
        else:
            raise Exception('Пошел нах')

        if os.path.isfile(filename):
            with open(filename, 'r') as fd:
                yaml_content = fd.read()
            self._build_config(yaml_content)
        else:
            raise Exception('Пошел нах, где файл падла')

    def _build_config(self, yaml_content):
        yaml_content = self.__replace_env_variables(yaml_content)
        content = yaml.load(yaml_content, Loader=yaml.FullLoader)

        self.config = Config(**content)

    @staticmethod
    def __replace_env_variables(yaml_content):
        pattern = r'\$\{([^}^{]+)\}'

        def replacer(match):
            value = os.environ.get(match.group(1), '')
            return value

        return re.sub(pattern, replacer, yaml_content)
