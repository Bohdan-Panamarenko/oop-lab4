from abc import abstractmethod, ABC
from typing import List


class ITeacher(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    # @abstractmethod
    # def name(self, value: str):
    #     pass

    # @abstractmethod
    # def has_topic(self, topic: Topic) -> bool:
    #     pass
    #
    # @abstractmethod
    # def add_topic(self, topic: Topic):
    #     pass
    #
    # @abstractmethod
    # def remove_topic(self, topic: Topic):
    #     pass

    @abstractmethod
    def courses(self) -> List[str]:
        pass

    def list_courses(self) -> str:
        pass

    @abstractmethod
    def __str__(self):
        pass


class ICourse(ABC):
    @abstractmethod
    def teachers(self) -> List[ITeacher]:
        pass

    @abstractmethod
    def list_teachers(self) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    # @abstractmethod
    # def name(self, value: str):
    #     pass

    # @abstractmethod
    # def add_topic(self, topic: Topic):
    #     pass

    # @abstractmethod
    # def remove_topic(self, order: int):
    #     pass

    @abstractmethod
    def topics(self) -> List[str]:
        pass

    @abstractmethod
    def list_topics(self) -> str:
        pass


class ILocalCourse(ABC):
    @abstractmethod
    def lab_number(self) -> int:
        pass


class IOffsiteCourse(ABC):
    @abstractmethod
    def city(self) -> str:
        pass


class ICourseFactory(ABC):
    @abstractmethod
    def local_courses(self) -> List[ILocalCourse]:
        pass

    @abstractmethod
    def offsite_courses(self) -> List[IOffsiteCourse]:
        pass

    @abstractmethod
    def teachers(self) -> List[ITeacher]:
        pass

    @abstractmethod
    def get_course_by_name(self, name: str) -> ICourse:
        pass

