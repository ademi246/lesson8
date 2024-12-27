import sqlite3


def create_connection(hw_db):
    connection = None
    try:
        connection = sqlite3.connect(hw_db)
    except sqlite3.Error as e:
        print(e)
    return connection


def get_cities(connection):
    try:
        get ='''SELECT ct_id, title FROM cities'''
        cursor = connection.cursor()
        cursor.execute(get)
        return cursor.fetchall()
    except sqlite3.Error as error :
        print(f'{error} Ошибка в get_cities')


def get_students_by_city(connection, ct_id):
    try:
        query = '''SELECT students.first_name, students.last_name,
        cities.title, cities.area
        FROM students 
        INNER JOIN cities ON students.city_id = cities.ct_id
        WHERE cities.ct_id = ?'''
        cursor = connection.cursor()
        cursor.execute(query, (ct_id,))
        return cursor.fetchall()
    except sqlite3.Error as error :
        print(f'{error} Произошла ошибка в get_students_by_city')

def main():
    connection = create_connection('data_base')
    if not connection:
        print('не удалось подключится к базе данных')
        return

    while True:
        print('Вы можете отобразить список учеников по выбранному id города из перечня городов ниже,\n'
              ' для выхода из программы введите 0:')
        cities = get_cities(connection)
        if not cities:
            print('Произошла ошибка')
            break
        for city in cities:
            print(f'{city[0]}, {city[1]}')
        try:
            city_id = int(input('введите id города'))
            if city_id == 0:
                break

        except ValueError:
            print('Произошла ошибка, пожалуйста попробуйте снова.')

        students = get_students_by_city(connection, city_id)
        if not students:
            print(f'В городе с id {city_id} нет учеников или неверный id.')

        else:
            print('\nСписок учеников:')
        for student in students: print(
            f'Имя: {student[0]}, Фамилия: {student[1]},\n'
            f'Город: {student[2]}, Площадь города: {student[3]} км², ')

    connection.close()

if "__name__" == "main":
     main()