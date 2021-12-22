from part2.interfaces.i_local_course import ILocalCourse
from part2.classes.course import Course


class LocalCourse(Course, ILocalCourse):
    """Describes local course"""

    def __init__(self, name, teachers, topics, lab_number):
        super().__init__(name, teachers, topics)
        self.__set_lab_number(lab_number)

    @property
    def lab_number(self) -> int:
        return self.__lab_number

    def __set_lab_number(self, value: int):
        """Private setter for lab number with validation"""
        if not isinstance(value, int):
            raise ValueError("laboratory number should be of type int")
        if value < 0:
            raise ValueError("laboratory number can not be negative")
        self.__lab_number = value

    def __str__(self):
        return super().__str__() + f"\nLaboratory number: {self.lab_number}"