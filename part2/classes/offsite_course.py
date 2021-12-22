from part2.interfaces.i_offsite_course import IOffsiteCourse
from part2.classes.course import Course


class OffsiteCourse(Course, IOffsiteCourse):
    """Describes offsite course"""

    def __init__(self, name, teachers, topics, city):
        super().__init__(name, teachers, topics)
        self.__set_city(city)

    @property
    def city(self) -> str:
        return self.__city

    def __set_city(self, value: str):
        """Private setter for city with validation"""
        if not isinstance(value, str):
            raise ValueError("city should be of type string")
        if not value:
            raise ValueError("city can not be empty")
        self.__city = value

    def __str__(self):
        return super().__str__() + f"\nGoing in city: {self.city}"