from abc import abstractmethod, ABC


class ILocalCourse(ABC):
    """Base interface of ILocalCourse"""
    @abstractmethod
    def lab_number(self) -> int:
        """Get number of laboratory where the course is going"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Get description of the local course"""
        pass

