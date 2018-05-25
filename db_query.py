from db import *


successful_result = 'Операция выполнена успешно'
person_error = 'Участника с таким именем не существует: {} {}'


def add_user(new_name, new_surname, new_chat_id):
    person = Participant.select().where(
        Participant.chat_id == new_chat_id,
        Participant.name == new_name,
        Participant.surname == new_surname)
    if len(person) == 0:
        Participant.create(name=new_name, surname=new_surname, chat_id=new_chat_id)
        return 'Новый участник успешно добавлен'
    return 'Участник с таким именем уже существует'
    

def all_users(chat_id):
    users = Participant.select().where(Participant.chat_id == chat_id)
    names = []
    surnames = []
    for user in users:
        names.append(user.name)
        surnames.append(user.surname)
    if len(names) == 0:
        return 'Ни один пользователь еще не добавлен'
    result = ''
    for i in range(len(names)):
        result += '{}. {} {}\n'.format((i + 1), names[i], surnames[i])
    return result


def get_all(chat_id):
    queries = Indebtedness.select().where(Indebtedness.chat_id == chat_id, Indebtedness.debt > 0)
    if len(queries) == 0:
        return "На данный момент нет задолженностей"
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
        index += 1
    return result


def get_all_debts(_name, _surname, chat_id):
    '''
    Возвращает имена должников и сумму долга.
    '''
    if not exist(_name, _surname, chat_id):
        return '{} {} отсутствует среди участников'.\
              format(_name, _surname)
    human = Participant.get(
        Participant.name == _name, Participant.surname == _surname,
        Participant.chat_id == chat_id)
    human_id = human.id
    people = Indebtedness.select().where(
        Indebtedness.from_id == human_id, Indebtedness.chat_id == chat_id,
        Indebtedness.debt > 0)
    if len(people) == 0:
        return 'Должников нет.'
    result = 'Должники({} {}):\n'.format(_name, _surname)
    index = 0
    for human in people:
        result += '{}. {} {} - {}\n'.format(
            index + 1, human.to_id.name, human.to_id.surname, human.debt)
    return result


def get_all_undebts(_name, _surname, chat_id):
    '''
    Возвращает имена тех, кому должен участник, и размер задолженности.
    '''
    if not exist(_name, _surname, chat_id):
        return '{} {} отсутствует среди участников'.\
              format(_name, _surname)
    human = Participant.get(
        Participant.name == _name, Participant.surname == _surname,
        Participant.chat_id == chat_id)
    human_id = human.id
    people = Indebtedness.select().where(
        Indebtedness.to_id == human_id, Indebtedness.chat_id == chat_id,
        Indebtedness.debt > 0)
    if len(people) == 0:
        return 'Задолженностей нет.'
    result = 'Задолженности({} {}):\n'.format(_name, _surname)
    index = 0
    for human in people:
        result += '{}. {} {} - {}\n'.format(
            index + 1, human.from_id.name, human.from_id.surname, human.debt)
    return result


def select_debt(from_name, from_surname, to_name, to_surname, chat_id):
    from_id = Participant.select().where(
        Participant.chat_id == chat_id,
        Participant.name == from_name,
        Participant.surname == from_surname).limit(1)

    if len(from_id):
        from_id = from_id[0]

        to_id = Participant.select().where(
            Participant.chat_id == chat_id,
            Participant.name == to_name,
            Participant.surname == to_surname).limit(1)
        if len(to_id):
            to_id = to_id[0]

            debts = Indebtedness.select().where(
                Indebtedness.chat_id == chat_id,
                Indebtedness.from_id == from_id,
                Indebtedness.to_id == to_id)

            if len(debts):
                debt = debts[0]
                return 'Задолженность:\n\t{} {} - {}'.format(
                    debt.to_id.name, debt.to_id.surname, debt.debt)
            else:
                return 'Данная запись отсутствует'
        else:
            return person_error.format(to_name, to_surname)
    else:
        return person_error.format(from_name, from_surname)


def create_debt(from_name, from_surname, to_name, to_surname, value, chat_id):
    if not exist(from_name, from_surname, chat_id):
        return '{} {} отсутствует среди участников'.\
              format(from_name, from_surname)
    if not exist(to_name, to_surname, chat_id):
        return '{} {} отсутствует среди участников'.format(to_name, to_surname)
    if value == 0:
        return('Введите сумму задолженности\n')
    if value > 0:
        from_id = Participant.select().where(
            Participant.chat_id == chat_id,
            Participant.name == from_name,
            Participant.surname == from_surname).limit(1)

        if len(from_id):
            from_id = from_id[0]

            to_id = Participant.select().where(
                Participant.chat_id == chat_id,
                Participant.name == to_name,
                Participant.surname == to_surname).limit(1)
            if len(to_id):
                to_id = to_id[0]
                query = Indebtedness.select().where(
                    Indebtedness.chat_id == chat_id,
                    Indebtedness.from_id == from_id,
                    Indebtedness.to_id == to_id,
                    Indebtedness.debt > 0).limit(1)
                if len(query):
                    query = query[0]
                    query.debt += value
                    query.save()
                    return 'Запись успешно обновлена\n'
                else:
                    Indebtedness.create(
                        from_id=from_id, to_id=to_id, debt=value, chat_id=chat_id)
                    return 'Запись успешно добавлена\n'
            else:
                return person_error.format(to_name, to_surname)
        else:
            return person_error.format(from_name, from_surname)
    if value < 0:
        create_debt(to_name, to_surname, from_name, from_surname, -value, chat_id)


def exist(name, surname, chat_id):
    try:
        person_id = Participant.get(
            chat_id == chat_id, name == name, surname == surname)
    except Exception:
        return False
    return True


def update_debt(from_name, from_surname, to_name, to_surname, value, chat_id):
    if not exist(from_name, from_surname, chat_id):
        return '{} {} отсутствует среди участников'.\
              format(from_name, from_surname)
    if not exist(to_name, to_surname, chat_id):
        return '{} {} отсутствует среди участников'.format(to_name, to_surname)
    if value == 0:
        return
    if value > 0:
        #
        # Первый user
        #
        from_id = Participant.select().where(
            Participant.chat_id == chat_id,
            Participant.name == from_name,
            Participant.surname == from_surname)
        if len(from_id):
            from_id = from_id[0]

            #
            # Второй user
            #
            to_id = Participant.select().where(
                Participant.chat_id == chat_id,
                Participant.name == to_name,
                Participant.surname == to_surname)

            if len(to_id):
                to_id = to_id[0]

                #
                # Запрос to_from
                #
                to_from = Indebtedness.select().where(
                    Indebtedness.chat_id == chat_id,
                    Indebtedness.from_id == to_id.id,
                    Indebtedness.to_id == from_id.id)

                if len(to_from):
                    to_from = to_from[0]

                    if value <= to_from.debt:
                        to_from.debt -= value
                        to_from.save()
                        return successful_result

                    new_value = value - to_from.debt
                    to_from.debt = 0
                    to_from.save()

                    #
                    # Запрос from_to
                    #
                    from_to = Indebtedness.select().where(
                        Indebtedness.chat_id == chat_id,
                        Indebtedness.from_id == from_id.id,
                        Indebtedness.to_id == to_id.id)

                    if len(from_to):
                        from_to = from_to[0]
                        from_to.debt += new_value
                        from_to.save()
                    else:
                        result = create_debt(
                            from_id.name, from_id.surname,
                            to_id.name, to_id.surname, new_value, chat_id)
                        return result + successful_result
                else:
                    #
                    # Запрос from_to
                    #
                    from_to = Indebtedness.select().where(
                        Indebtedness.chat_id == chat_id,
                        Indebtedness.from_id == from_id.id,
                        Indebtedness.to_id == to_id.id)
                    if len(from_to):
                        from_to = from_to[0]
                        from_to.debt += value
                        from_to.save()
                    else:
                        result = create_debt(
                            from_id.name, from_id.surname,
                            to_id.name, to_id.surname, value, chat_id)
                        return '{}\n{}'.format(result, successful_result)
                return successful_result
            else:
                return person_error.format(to_name, to_surname)
        else:
            return person_error.format(from_name, from_surname)
    else:
        return update_debt(
            to_name, to_surname, from_name, from_surname, -value, chat_id)
