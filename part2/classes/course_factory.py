import sqlite3
from os.path import exists
from typing import List

from part2.classes.course import Course
from part2.classes.local_course import LocalCourse
from part2.classes.offsite_course import OffsiteCourse
from part2.classes.teacher import Teacher
from part2.interfaces.i_course import ICourse
from part2.interfaces.i_course_factory import ICourseFactory
from part2.interfaces.i_local_course import ILocalCourse
from part2.interfaces.i_offsite_course import IOffsiteCourse
from part2.interfaces.i_teacher import ITeacher


class CourseFactory(ICourseFactory):
    """Describes course factory which connects to database and produce courses and teachers"""

    def __init__(self, database: str):
        if not isinstance(database, str):
            raise ValueError("database path should be of type string")
        if not exists(database):
            raise ValueError("database does not exists")

        self.__db = database

    def __call_to_db(self, call: str, *args):
        """Makes call to database and returns its response"""
        if not isinstance(call, str):
            raise ValueError("call should be of type string")
        db = sqlite3.connect(self.__db)
        response = db.cursor().execute(call, args).fetchall()
        db.close()
        return response

    def __get_topics_by_course_id(self, course_id: int):
        """Request topics which has course with specific course id"""
        if not isinstance(course_id, int):
            raise ValueError("course_id should be of type int")

        topics = self.__call_to_db("SELECT topics.name FROM course_topic INNER JOIN courses ON course_topic.course_id"
                                   " = courses.id INNER JOIN topics ON course_topic.topic_id = topics.id "
                                   "WHERE courses.id=? ORDER BY topic_order;", course_id)
        return list((t[0] for t in topics))

    def __get_courses_names_by_teacher_id(self, teacher_id: int):
        """Request courses which has teacher with specific id"""
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

    def get_course_by_name(self, name: str) -> ICourse:
        if not isinstance(name, str):
            raise ValueError("course name should be of type string")

        course_id = self.__call_to_db("SELECT id FROM courses WHERE name = ?;", name)

        if not course_id:
            raise ValueError("course with such name does not exist")

        topics = self.__get_topics_by_course_id(course_id[0][0])
        return Course(name, [], topics)
