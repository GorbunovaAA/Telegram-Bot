from db import *
successful_result = 'Операция выполнена успешно'


def add_user(new_name, new_surname):
    person = Participant.select().where((Participant.name == new_name) &
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
        # print('user_id = {}'.format(user.id))
    if len(names) == 0:
        return [], []
    if len(surnames) == 0:
        return [], []
    return names, surnames


def get_all_debts(name, surname):
    people = Participant.get(name=name,
                             surname=surname).get().to_id
    human_list = []
    debt_list = []
    for human in people:
        human_list.append([human.from_id.name, human.from_id.surname])
        debt_list.append(human.debt)
    print(*human_list)
    print(*debt_list)
    return human_list, debt_list


def get_all_undebts(name, surname):
    people = Participant.get(name=name,
                             surname=surname).get().from_id
    human_list = []
    debt_list = []
    for human in people:
        human_list.append([human.to_id.name, human.to_id.surname])
        debt_list.append(human.debt)
    print(*human_list)
    print(*debt_list)
    return human_list, debt_list


def ask_debt(from_name, from_surname, to_name, to_surname):
    if not exist(from_name, from_surname):
        return 'First person is not avaliable'
    if not exist(to_name, to_surname):
        return 'Second person is not avaliable'
    try:
        debt = select_debt(from_name, from_surname, to_name, to_surname)
    except Exception:
        return 0
    return debt[4]


def select_debt(from_name, from_surname, to_name, to_surname):
    from_id = Participant.\
              select().where(Participant.name == from_name,
                             Participant.surname == from_surname).limit(1)[0]
    to_id = Participant.select().
    where(Participant.name == to_name,
          Participant.surname == to_surname).limit(1)[0]
    debts = Indebtedness.select().where(Indebtedness.from_id == from_id,
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
        # print(debt.from_id.name, debt.from_id.surname,\
        #  debt.to_id.name, debt.to_id.surname, debt.debt)
    return (from_names[0], from_surnames[0], to_names[0],
            to_surnames[0], value[0])


def create_debt(from_name, from_surname, to_name, to_surname, value=0):
    if value == 0:
        print('Введите сумму задолженности')
    if value > 0:
        from_id = Participant.select().where(Participant.name == from_name,
                                             Participant.surname ==
                                             from_surname).limit(1)[0]
        to_id = Participant.select().where(Participant.name == to_name,
                                           Participant.surname ==
                                           to_surname).limit(1)[0]
        try:
            query = Indebtedness.select().
            where(Indebtedness.from_id == from_id, Indebtedness.to_id == to_id,
                  Indebtedness.debt > 0).limit(1)[0]
            query.debt += value
            query.save()
        except Exception:
            Indebtedness.create(from_id=from_id, to_id=to_id, debt=value)
    if value < 0:
        create_debt(to_name, to_surname, from_name, from_surname, -value)
    # debts = Indebtedness.select()
    # for debt in debts:
    #   print(debt.from_id.name, debt.from_id.surname,\
    #    debt.to_id.name, debt.to_id.surname, debt.debt)


def exist(name, surname):
    try:
        person_id = Participant.get(name == name,
                                    surname == surname)
    except Exception:
        return False
    return True


def update_debt(from_name, from_surname, to_name, to_surname, value):
    if not exist(from_name, from_surname):
        print('{} {} отсутствует среди участников'.
              format(from_name, from_surname))
        return
    if not exist(to_name, to_surname):
        print('{} {} отсутствует среди участников'.format(to_name, to_surname))
        return
    if value == 0:
        return
    if value > 0:
        try:
            #
            # Первый user
            #
            from_id = Participant.get(Participant.name == from_name,
                                      Participant.surname == from_surname)
            try:
                #
                # Второй user
                #
                to_id = Participant.get(Participant.name == to_name,
                                        Participant.surname == to_surname)
                try:
                    #
                    # Запрос to_from
                    #
                    to_from = Indebtedness.select().
                    where(Indebtedness.from_id == to_id.id,
                          Indebtedness.to_id == from_id.id)[0]
                    new_value = max(value - to_from.debt, 0)
                    to_from.debt = max(to_from.debt - value, 0)
                    to_from.save()
                    return successful_result
                    try:
                        #
                        # Запрос from_to
                        #
                        from_to = Indebtedness.select().
                        where(Indebtedness.from_id == from_id.id,
                              Indebtedness.to_id == to_id.id)[0]
                        from_to.debt += new_value
                        from_to.save()
                    except Exception:
                        create_debt(from_id.name, from_id.surname,
                                    to_id.name, to_id.surname, new_value)
                        return successful_result
                except Exception:
                    try:
                        #
                        # Запрос from_to
                        #
                        from_to = Indebtedness.select().
                        where(Indebtedness.from_id == from_id.id,
                              Indebtedness.to_id == to_id.id)[0]
                        from_to.debt += value
                        from_to.save()
                        return successful_result
                    except Exception:
                        create_debt(from_id.name, from_id.surname,
                                    to_id.name, to_id.surname, value)
                        return successful_result
            except Exception:
                print('Второй участник не добавлен.\n'
                      'Повторите запрос с корректными данными')
                return
        except Exception:
            print('Первый участник не добавлен.\n'
                  'Повторите запрос с корректными данными')
            return
    else:
        update_debt(to_name, to_surname, from_name, from_surname, -value)
