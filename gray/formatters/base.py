from abc import ABC, abstractmethod
from pathlib import Path

from configargparse import Namespace


class BaseFormatter(ABC):

    def __init__(self, arguments: Namespace):
        pass

    @abstractmethod
    def process(self, file_path: Path):
        pass
