from classes import CourseFactory

cf = CourseFactory("./database.db")


def list_items(lst):
    for item in lst:
        print(item)
        print("----------")


# actions = {
#     1: list_items(cf.teachers),
#     2: list_items(cf.local_courses),
#     3: list_items(cf.offsite_courses),
#     4: exit(0)
# }


while True:
    print("\n\nAllowed actions:")
    print("1. List all teachers")
    print("2. List all local courses")
    print("3. List all offsite courses")
    print("4. Exit")

    try:
        x = int(input("Number: "))
    except Exception as e:
        print(e)
        continue

    if x == 1:
        list_items(cf.teachers)
    elif x == 2:
        list_items(cf.local_courses)
    elif x == 3:
        list_items(cf.offsite_courses)
    elif x == 4:
        exit(0)
    else:
        print("->> Invalid command code")





