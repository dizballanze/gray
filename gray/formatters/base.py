from abc import ABC, abstractmethod
from pathlib import Path


class BaseFormatter(ABC):

    @abstractmethod
    def process(self, file_path: Path):
        pass
