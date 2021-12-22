from part2.interfaces.i_teacher import ITeacher
from re import match
from typing import List
from copy import copy


class Teacher(ITeacher):
    """Describes teacher"""

    def __init__(self, name: str, courses: List[str]):
        self.__set_name(name)
        self.__set_courses(courses)

    @property
    def name(self) -> str:
        return self.__name

    def __set_name(self, value: str):
        """Private setter for name with validation"""
        if not isinstance(value, str):
            raise ValueError("name should be of type string")
        if match("[^a-zA-Zа-яА-Я\\s]", value) or len(value) == 0:
            raise ValueError("name field should store name")
        self.__name = value

    @property
    def courses(self) -> List[str]:
        return copy(self.__courses)

    @property
    def list_courses(self) -> str:
        return ", ".join(self.__courses)

    def __set_courses(self, value: List[str]):
        """Private setter for courses with validation"""
        for c in value:
            if not isinstance(c, str):
                raise ValueError("should contain only course names of type str")
        self.__courses = value

    def __str__(self):
        return f"{self.name} ведёт курсы: {self.list_courses}"