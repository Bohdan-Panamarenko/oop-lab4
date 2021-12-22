from abc import abstractmethod, ABC


class IOffsiteCourse(ABC):
    """Base interface of offsite course"""
    @abstractmethod
    def city(self) -> str:
        """Get city name where the course is going"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Get description of the offsite course"""
        pass

