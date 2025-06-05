import os
import re

import yaml

from src.config.config import Config
from src.extensions import Singleton


class Settings(metaclass=Singleton):
    def __init__(self):
        env = os.getenv("MODE", "test")

        if env in ['dev', 'prod']:
            filename = 'config.yaml'
        elif env == "test":
            filename = 'test-config.yaml'
        else:
            raise Exception(f"Неверный параметр запуска. ожидалось prod или test, получено {env}")

        if os.path.isfile(filename):
            with open(filename, 'r') as fd:
                yaml_content = fd.read()
            self._build_config(yaml_content)
        else:
            raise Exception(f'{filename} отсутствует')

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
