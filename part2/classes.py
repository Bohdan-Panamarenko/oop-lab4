import copy
from os.path import exists

from interfaces import *
from re import match

import sqlite3


class Teacher(ITeacher):

    def __init__(self, name: str, courses: List[str]):
        self.__set_name(name)
        self.__set_courses(courses)

    @property
    def name(self) -> str:
        return self.__name

    def __set_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("name should be of type string")
        if match("[^a-zA-Zа-яА-Я\\s]", value) or len(value) == 0:
            raise ValueError("name field should store name")
        self.__name = value

    @property
    def courses(self) -> List[str]:
        return copy.copy(self.__courses)

    @property
    def list_courses(self) -> str:
        return ", ".join(self.__courses)

    def __set_courses(self, value: List[str]):
        for c in value:
            if not isinstance(c, str) or not c:
                raise ValueError
        self.__courses = value

    # def has_topic(self, topic: Topic) -> bool:
    #     if not isinstance(topic, Topic):
    #         raise ValueError("topic should be object of class Topic")
    #     return topic in self.topics
    #
    # def add_topic(self, topic: Topic):
    #     if not isinstance(topic, Topic):
    #         raise ValueError("topic should be object of class Topic")
    #     if self.has_topic(topic):
    #         raise ValueError(f"teacher {self.name} already has topic {topic.value}")
    #
    #     self.topics.add(topic)
    #
    # def remove_topic(self, topic: Topic):
    #     if not isinstance(topic, Topic):
    #         raise ValueError("topic should be object of class Topic")
    #     if not self.has_topic(topic):
    #         raise ValueError(f"teacher {self.name} does not have topic {topic.value}")
    #
    #     self.topics.remove(topic)

    def __str__(self):
        return f"{self.name} ведёт курсы: {self.list_courses}"


class Course(ICourse):
    def __init__(self, name, teachers, topics):
        self.__set_name(name)
        self.__set_teachers(teachers)
        self.__set_topics(topics)

    def __set_teachers(self, value: List[ITeacher]):
        for teacher in value:
            if not isinstance(teacher, ITeacher):
                raise ValueError
        self.__teachers = value

    @property
    def teachers(self) -> List[ITeacher]:
        return copy.copy(self.__teachers)

    @property
    def list_teachers(self) -> str:
        x = (f"--> {t.__str__()}" for t in self.__teachers)
        return "\n".join(x)

    @property
    def name(self) -> str:
        return self.__name

    # @name.setter
    def __set_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("name should be of type string")
        if not value:
            raise ValueError("name can not be empty")
        self.__name = value

    def __set_topics(self, value: List[str]):
        for t in value:
            if not isinstance(t, str):
                raise ValueError
        self.__topics = value

    @property
    def topics(self) -> List[str]:
        return copy.copy(self.__topics)

    @property
    def list_topics(self) -> str:
        x = (t.__str__() for t in self.__topics)
        return ", ".join(x)

    def __str__(self):
        return f"{self.name}\nTeachers:\n{self.list_teachers}\nProgram: {self.list_topics}"


class LocalCourse(Course, ILocalCourse):
    def __init__(self, name, teachers, topics, lab_number):
        super().__init__(name, teachers, topics)
        self.__set_lab_number(lab_number)

    @property
    def lab_number(self) -> int:
        return self.__lab_number

    def __set_lab_number(self, value: int):
        if not isinstance(value, int):
            raise ValueError("laboratory number should be of type int")
        if value < 0:
            raise ValueError("laboratory number can not be negative")
        self.__lab_number = value

    def __str__(self):
        return super().__str__() + f"\nLaboratory number: {self.lab_number}"


class OffsiteCourse(Course, IOffsiteCourse):
    def __init__(self, name, teachers, topics, city):
        super().__init__(name, teachers, topics)
        self.__set_city(city)

    @property
    def city(self) -> str:
        return self.__city

    def __set_city(self, value: str):
        if not isinstance(value, str):
            raise ValueError("city should be of type string")
        if not value:
            raise ValueError("city can not be empty")
        self.__city = value

    def __str__(self):
        return super().__str__() + f"\nGoing in city: {self.city}"


class CourseFactory(ICourseFactory):
    def __init__(self, database: str):
        if not isinstance(database, str):
            raise ValueError("database path should be of type string")
        if not exists(database):
            raise ValueError("database does not exists")

        self.__db = database

    def __call_to_db(self, call: str, *args):
        if not isinstance(call, str):
            raise ValueError("call should be of type string")
        db = sqlite3.connect(self.__db)
        response = db.cursor().execute(call, args).fetchall()
        db.close()
        return response

    def __get_topics_by_course_id(self, course_id: int):
        if not isinstance(course_id, int):
            raise ValueError

        topics = self.__call_to_db("SELECT topics.name FROM course_topic INNER JOIN courses ON course_topic.course_id"
                                   " = courses.id INNER JOIN topics ON course_topic.topic_id = topics.id "
                                   "WHERE courses.id=? ORDER BY topic_order;", course_id)
        return list((t[0] for t in topics))

    def __get_courses_names_by_teacher_id(self, teacher_id: int):
        if not isinstance(teacher_id, int):
            raise ValueError

        courses_info = self.__call_to_db("SELECT courses.name FROM teacher_course "
                                         "INNER JOIN courses ON teacher_course.course_id = courses.id "
                                         "WHERE teacher_course.teacher_id = ?;", teacher_id)

        return list((c[0] for c in courses_info))

    @property
    def local_courses(self) -> List[ILocalCourse]:
        courses = list()
        local_courses_info = self.__call_to_db("SELECT courses.id, local_courses.id, name, laboratory_number FROM local_courses "
                                               "INNER JOIN courses ON local_courses.course_id = courses.id")

        for local_course in local_courses_info:
            topics = self.__get_topics_by_course_id(local_course[0])

            teachers_info = self.__call_to_db("SELECT teachers.id, first_name, last_name, patronymic FROM teacher_local_course "
                                         "INNER JOIN local_courses ON teacher_local_course.local_course_id = local_courses.id "
                                         "INNER JOIN teachers ON teacher_local_course.teacher_id = teachers.id "
                                         "WHERE local_course_id = ?;", local_course[1])

            teachers = list()
            for teacher in teachers_info:
                teachers.append(Teacher(f"{teacher[1]} {teacher[2]} {teacher[3]}", self.__get_courses_names_by_teacher_id(teacher[0])))

            courses.append(LocalCourse(local_course[2], teachers, topics, local_course[3]))

        return courses

    @property
    def offsite_courses(self) -> List[IOffsiteCourse]:
        courses = list()
        offsite_courses_info = self.__call_to_db(
            "SELECT courses.id, offsite_courses.id, name, city FROM offsite_courses "
            "INNER JOIN courses ON offsite_courses.course_id = courses.id")

        for offsite_course in offsite_courses_info:
            topics = self.__get_topics_by_course_id(offsite_course[0])

            teachers_info = self.__call_to_db("SELECT teachers.id, first_name, last_name, patronymic FROM teacher_offsite_course "
                                              "INNER JOIN offsite_courses ON teacher_offsite_course.offsite_course_id = offsite_courses.id "
                                              "INNER JOIN teachers ON teacher_offsite_course.teacher_id = teachers.id "
                                              "WHERE offsite_course_id = ?;", offsite_course[1])

            teachers = list()
            for teacher in teachers_info:
                teachers.append(Teacher(f"{teacher[1]} {teacher[2]} {teacher[3]}", self.__get_courses_names_by_teacher_id(teacher[0])))

            courses.append(OffsiteCourse(offsite_course[2], teachers, topics, offsite_course[3]))

        return courses

    @property
    def teachers(self) -> List[ITeacher]:
        teachers = list()
        response = self.__call_to_db("SELECT id, first_name, last_name, patronymic FROM teachers;")

        for teacher in response:
            teachers.append(Teacher(f"{teacher[1]} {teacher[2]} {teacher[3]}", self.__get_courses_names_by_teacher_id(teacher[0])))

        return teachers


