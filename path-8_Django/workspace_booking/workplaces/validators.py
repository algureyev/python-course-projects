from django.core.exceptions import ValidationError


def validate_developer_tester_neighbors(workplace):
    """
    Простой валидатор по заданной логике
    """
    from workplaces.models import Workplace

    print("=== НАЧАЛО ВАЛИДАЦИИ ===")
    print(f"Проверяем стол: {workplace.table_number}")
    print(f"Новый сотрудник: {workplace.employee}")

    # Сохраняем текущее состояние из базы
    try:
        current_workplace = Workplace.objects.get(id=workplace.id)
        old_employee = current_workplace.employee
        print(f"Старый сотрудник: {old_employee}")
    except Workplace.DoesNotExist:
        old_employee = None
        print("Новый стол (не было старого сотрудника)")

    # Условно применяем новое состояние для проверки
    temp_employee = workplace.employee

    print(f"Временное состояние: {temp_employee}")

    # ПРОВЕРКА 1: Если новое состояние пустота - проверка пройдена
    if not temp_employee:
        print("✅ Проверка пройдена: стол пустой")
        return

    # Получаем навыки нового работника
    new_employee_skills = [skill.name for skill in temp_employee.skills.all()]
    print(f"Навыки нового работника: {new_employee_skills}")

    # ПРОВЕРКА 2: Если навыки не Тестирование, Бэкенд, Фронтэнд - проверка пройдена
    if not any(
        skill in new_employee_skills for skill in ["Тестирование", "Бэкенд", "Фронтэнд"]
    ):
        print("✅ Проверка пройдена: сотрудник не разработчик и не тестировщик")
        return

    # Определяем роль нового сотрудника
    is_tester = "Тестирование" in new_employee_skills
    is_developer = any(skill in new_employee_skills for skill in ["Бэкенд", "Фронтэнд"])

    print(f"Роль: тестировщик={is_tester}, разработчик={is_developer}")

    # Проверяем соседние столы
    table_num = workplace.table_number
    left_table_num = table_num - 1
    right_table_num = table_num + 1

    print(f"Соседние столы: слева={left_table_num}, справа={right_table_num}")

    # Получаем соседние столы
    left_workplace = None
    right_workplace = None

    try:
        left_workplace = Workplace.objects.get(table_number=left_table_num)
        print(f"Левый сосед: {left_workplace.employee}")
    except Workplace.DoesNotExist:
        print("Левого соседа нет")

    try:
        right_workplace = Workplace.objects.get(table_number=right_table_num)
        print(f"Правый сосед: {right_workplace.employee}")
    except Workplace.DoesNotExist:
        print("Правого соседа нет")

    # Проверяем левого соседа
    if left_workplace and left_workplace.employee:
        left_skills = [skill.name for skill in left_workplace.employee.skills.all()]
        left_is_tester = "Тестирование" in left_skills
        left_is_developer = any(
            skill in left_skills for skill in ["Бэкенд", "Фронтэнд"]
        )

        print(
            f"Левый сосед - тестировщик: {left_is_tester}, разработчик: {left_is_developer}"
        )

        # ПРОВЕРКА 3: Если новый - тестировщик, а слева - разработчик -> ОШИБКА
        if is_tester and left_is_developer:
            print("❌ Ошибка: тестировщик слева от разработчика")
            workplace.employee = old_employee  # Возвращаем старое состояние
            raise ValidationError(
                "Нельзя размещать тестировщика слева от разработчика!"
            )

        # ПРОВЕРКА 4: Если новый - разработчик, а слева - тестировщик -> ОШИБКА
        if is_developer and left_is_tester:
            print("❌ Ошибка: разработчик слева от тестировщика")
            workplace.employee = old_employee  # Возвращаем старое состояние
            raise ValidationError(
                "Нельзя размещать разработчика слева от тестировщика!"
            )

    # Проверяем правого соседа
    if right_workplace and right_workplace.employee:
        right_skills = [skill.name for skill in right_workplace.employee.skills.all()]
        right_is_tester = "Тестирование" in right_skills
        right_is_developer = any(
            skill in right_skills for skill in ["Бэкенд", "Фронтэнд"]
        )

        print(
            f"Правый сосед - тестировщик: {right_is_tester}, разработчик: {right_is_developer}"
        )

        # ПРОВЕРКА 5: Если новый - тестировщик, а справа - разработчик -> ОШИБКА
        if is_tester and right_is_developer:
            print("❌ Ошибка: тестировщик справа от разработчика")
            workplace.employee = old_employee  # Возвращаем старое состояние
            raise ValidationError(
                "Нельзя размещать тестировщика справа от разработчика!"
            )

        # ПРОВЕРКА 6: Если новый - разработчик, а справа - тестировщик -> ОШИБКА
        if is_developer and right_is_tester:
            print("❌ Ошибка: разработчик справа от тестировщика")
            workplace.employee = old_employee  # Возвращаем старое состояние
            raise ValidationError(
                "Нельзя размещать разработчика справа от тестировщика!"
            )

    print("✅ Все проверки пройдены успешно")
    print("=== КОНЕЦ ВАЛИДАЦИИ ===")
