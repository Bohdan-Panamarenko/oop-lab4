from abc import abstractmethod, ABC
from typing import List
from part2.interfaces.i_teacher import ITeacher


class ICourse(ABC):
    """Describes base interface of course"""
    @abstractmethod
    def teachers(self) -> List[ITeacher]:
        """Get list of teachers of the course"""
        pass

    @abstractmethod
    def list_teachers(self) -> str:
        """Get string with teachers description of the course"""
        pass

    @abstractmethod
    def name(self) -> str:
        """Get name of the course"""
        pass

    @abstractmethod
    def topics(self) -> List[str]:
        """Get list of topics of the course"""
        pass

    @abstractmethod
    def list_topics(self) -> str:
        """Get string with topics description of the course"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Get description of the course"""
        pass

