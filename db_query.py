from db import *


successful_result = 'Операция выполнена успешно'
first_person_error = '(1) Участника с таким именем не существует'
second_person_error = '(2) Участника с таким именем не существует'

def change_db(chat_id):
    db = SqliteDatabase('people{}.db'.format(chat_id))
    db.create_tables([Participant, Currency, Indebtedness])
    db.close()
    

def add_user(new_name, new_surname):
    person = Participant.select().where(
        (Participant.name == new_name) &
        (Participant.surname == new_surname))
    if len(person) == 0:
        Participant.create(name=new_name, surname=new_surname)
        return 'Новый участник успешно добавлен'
    return 'Участник с таким именем уже существует'


def all_users():
    users = Participant.select()
    names = []
    surnames = []
    for user in users:
        names.append(user.name)
        surnames.append(user.surname)
    if len(names) == 0:
        return [], []
    if len(surnames) == 0:
        return [], []
    return names, surnames


def get_all():
    queries = Indebtedness.select()
    if len(Indebtedness) == 0:
        return
    result = ''
    index = 0
    for query in queries:
        result += '{}. {} {}, {} {} - {}\n'.format(
            index + 1, query.from_id.name,
            query.from_id.surname,
            query.to_id.name,
            query.to_id.surname,
            query.debt
        )
    return result


def get_all_debts(_name, _surname):
    '''
    Возвращает имена должников и сумму долга.
    '''
    if not exist(_name, _surname):
        return '{} {} отсутствует среди участников'.\
              format(_name, _surname)
    human = Participant.get(
        Participant.name == _name, Participant.surname == _surname)
    human_id = human.id
    people = Indebtedness.select().where(Indebtedness.from_id == human_id)
    if len(people) == 0:
        return 'Должников нет.'
    result = 'Должники({} {}):\n'.format(_name, _surname)
    index = 0
    for human in people:
        result += '{}. {} {} - {}\n'.format(
            index + 1, human.to_id.name, human.to_id.surname, human.debt)
    return result


def get_all_undebts(_name, _surname):
    '''
    Возвращает имена тех, кому должен участник, и размер задолженности.
    '''
    if not exist(_name, _surname):
        return '{} {} отсутствует среди участников'.\
              format(_name, _surname)
    human = Participant.get(
        Participant.name == _name, Participant.surname == _surname)
    human_id = human.id
    people = Indebtedness.select().where(Indebtedness.to_id == human_id)
    if len(people):
        return 'Задолженностей нет.'
    result = 'Задолженности({} {}):\n'.format(_name, _surname)
    index = 0
    for human in people:
        result += '{}. {} {} - {}\n'.format(
            index + 1, human.from_id.name, human.from_id.surname, human.debt)
    return result


def select_debt(from_name, from_surname, to_name, to_surname):
    try:
        from_id = Participant.select().where(
            Participant.name == from_name,
            Participant.surname == from_surname).limit(1)[0]
        try:
            to_id = Participant.select().where(
                Participant.name == to_name,
                Participant.surname == to_surname).limit(1)[0]
            try:
                debts = Indebtedness.select().where(
                    Indebtedness.from_id == from_id,
                    Indebtedness.to_id == to_id)
                from_names = []
                from_surnames = []
                to_names = []
                to_surnames = []
                value = []
                for debt in debts:
                    from_names.append(debt.from_id.name)
                    from_surnames.append(debt.from_id.surname)
                    to_names.append(debt.to_id.name)
                    to_surnames.append(debt.to_id.surname)
                    value.append(debt.debt)
            except Exception:
                return 'Данная запись отсутствует'
            return 'Задолженность:\n\t{} {} - {}'.format(
                to_names[0], to_surnames[0], value[0])
        except Exception:
            return second_person_error
    except Exception:
        return first_person_error


def create_debt(from_name, from_surname, to_name, to_surname, value=0):
    if not exist(from_name, from_surname):
        return '{} {} отсутствует среди участников'.\
              format(from_name, from_surname)
    if not exist(to_name, to_surname):
        return '{} {} отсутствует среди участников'.format(to_name, to_surname)
    if value == 0:
        return('Введите сумму задолженности')
    if value > 0:
        try:
            from_id = Participant.select().where(
                Participant.name == from_name,
                Participant.surname == from_surname).limit(1)[0]
            try:
                to_id = Participant.select().where(
                    Participant.name == to_name,
                    Participant.surname == to_surname).limit(1)[0]
                try:
                    query = Indebtedness.select().where(
                        Indebtedness.from_id == from_id,
                        Indebtedness.to_id == to_id,
                        Indebtedness.debt > 0).limit(1)[0]
                    query.debt += value
                    query.save()
                except Exception:
                    Indebtedness.create(
                        from_id=from_id, to_id=to_id, debt=value)
                    return 'Запись успешно добавлена'
                return 'Запись успешно обновлена'
            except Exception:
                return second_person_error
        except Exception:
            return first_person_error
    if value < 0:
        create_debt(to_name, to_surname, from_name, from_surname, -value)


def exist(name, surname):
    try:
        person_id = Participant.get(
            name == name, surname == surname)
    except Exception:
        return False
    return True


def update_debt(from_name, from_surname, to_name, to_surname, value):
    if not exist(from_name, from_surname):
        return '{} {} отсутствует среди участников'.\
              format(from_name, from_surname)
    if not exist(to_name, to_surname):
        return '{} {} отсутствует среди участников'.format(to_name, to_surname)
    if value == 0:
        return
    if value > 0:
        try:
            #
            # Первый user
            #
            from_id = Participant.get(
                Participant.name == from_name,
                Participant.surname == from_surname)
            try:
                #
                # Второй user
                #
                to_id = Participant.get(
                    Participant.name == to_name,
                    Participant.surname == to_surname)
                try:
                    #
                    # Запрос to_from
                    #
                    to_from = Indebtedness.select().where(
                        Indebtedness.from_id == to_id.id,
                        Indebtedness.to_id == from_id.id)[0]
                    new_value = max(value - to_from.debt, 0)
                    to_from.debt = max(to_from.debt - value, 0)
                    to_from.save()
                    try:
                        #
                        # Запрос from_to
                        #
                        from_to = Indebtedness.select().where(
                            Indebtedness.from_id == from_id.id,
                            Indebtedness.to_id == to_id.id)[0]
                        from_to.debt += new_value
                        from_to.save()
                    except Exception:
                        result = create_debt(
                            from_id.name, from_id.surname,
                            to_id.name, to_id.surname, new_value)
                        return result + successful_result
                    return successful_results
                except Exception:
                    try:
                        #
                        # Запрос from_to
                        #
                        from_to = Indebtedness.select().where(
                            Indebtedness.from_id == from_id.id,
                            Indebtedness.to_id == to_id.id)[0]
                        from_to.debt += value
                        from_to.save()
                    except Exception:
                        result = create_debt(
                            from_id.name, from_id.surname,
                            to_id.name, to_id.surname, value)
                        return '{}\n{}'.format(result, successful_result)
                    return successful_result
                return successful_result
            except Exception:
                return second_person_error
        except Exception:
            return first_person_error
    else:
        return update_debt(
            to_name, to_surname, from_name, from_surname, -value)

