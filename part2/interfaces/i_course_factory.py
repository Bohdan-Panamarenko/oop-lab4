from abc import abstractmethod, ABC
from typing import List

from part2.interfaces.i_local_course import ILocalCourse
from part2.interfaces.i_offsite_course import IOffsiteCourse
from part2.interfaces.i_teacher import ITeacher
from part2.interfaces.i_course import ICourse


class ICourseFactory(ABC):
    """Describes base interface of course factory"""
    @abstractmethod
    def local_courses(self) -> List[ILocalCourse]:
        """Get list of all local courses"""
        pass

    @abstractmethod
    def offsite_courses(self) -> List[IOffsiteCourse]:
        """Get list of all offsite courses"""
        pass

    @abstractmethod
    def teachers(self) -> List[ITeacher]:
        """Get list of all teachers"""
        pass

    @abstractmethod
    def get_course_by_name(self, name: str) -> ICourse:
        """Get specific course by its name"""
        pass

