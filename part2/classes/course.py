from part2.interfaces.i_course import ICourse
from part2.interfaces.i_teacher import ITeacher
from copy import copy
from typing import List


class Course(ICourse):
    """Describes base course with program"""

    def __init__(self, name, teachers, topics):
        self.__set_name(name)
        self.__set_teachers(teachers)
        self.__set_topics(topics)

    def __set_teachers(self, value: List[ITeacher]):
        """Private setter for teachers with validation"""
        for teacher in value:
            if not isinstance(teacher, ITeacher):
                raise ValueError("should contain only object that implements ITeacher")
        self.__teachers = value

    @property
    def teachers(self) -> List[ITeacher]:
        return copy(self.__teachers)

    @property
    def list_teachers(self) -> str:
        x = (f"--> {t.__str__()}" for t in self.__teachers)
        return "\n".join(x)

    @property
    def name(self) -> str:
        return self.__name

    def __set_name(self, value: str):
        """Private setter for name with validation"""
        if not isinstance(value, str):
            raise ValueError("name should be of type string")
        if not value:
            raise ValueError("name can not be empty")
        self.__name = value

    def __set_topics(self, value: List[str]):
        """Private setter for topics with validation"""
        for t in value:
            if not isinstance(t, str):
                raise ValueError
        self.__topics = value

    @property
    def topics(self) -> List[str]:
        return copy(self.__topics)

    @property
    def list_topics(self) -> str:
        x = (t.__str__() for t in self.__topics)
        return ", ".join(x)

    def __str__(self):
        teachers = '\nTeachers: \n' + self.list_teachers if self.__teachers else ''
        return f"{self.name}{teachers}\nProgram: {self.list_topics}"