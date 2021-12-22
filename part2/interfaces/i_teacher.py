from abc import abstractmethod, ABC
from typing import List


class ITeacher(ABC):
    """Base interface of course"""
    @abstractmethod
    def name(self) -> str:
        """Get name of teacher"""
        pass

    @abstractmethod
    def courses(self) -> List[str]:
        """Get list of names of courses which the teacher knows"""
        pass

    @abstractmethod
    def list_courses(self) -> str:
        """Get string with sequence of courses which the teacher knows"""
        pass

    @abstractmethod
    def __str__(self):
        """Get description of the teacher"""
        pass


