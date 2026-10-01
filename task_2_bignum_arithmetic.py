M = 1000
N = 100

WIDTH = len(str(M - 1))   # ширина одного разряда при выводе (3 для M=1000)


def from_string(number):
    """Преобразует десятичную строку в длинное число.

    Parameters
    ----------
    number : str
        Десятичная запись целого числа, может начинаться с + или -.
        Пробелы по краям игнорируются.

    Returns
    -------
    sign : int
        Знак числа: 1 или -1. Для нуля всегда 1.
    digits : list of int
        Разряды числа в системе с основанием M, от старшего к младшему.

    Raises
    ------
    ValueError
        Если строка пустая или содержит недопустимые символы.
    OverflowError
        Если число содержит больше N разрядов.
    """

    number = number.strip()

    if not number:
        raise ValueError("Пустое число")

    sign = 1

    if number.startswith("-"):
        sign = -1
        number = number[1:]
    elif number.startswith("+"):
        number = number[1:]

    if not number:
        raise ValueError("Пустое число")

    if not number.isdigit():
        raise ValueError(f"Недопустимое число: {number}")

    number = number.lstrip("0") 

    if not number:
        return 1, [0]

    digits = [0]

    for char in number:
        decimal_digit = ord(char) - ord("0")

        carry = decimal_digit

        for i in range(len(digits) - 1, -1, -1):
            value = digits[i] * 10 + carry
            digits[i] = value % M
            carry = value // M

        if carry:
            digits.insert(0, carry)

        if len(digits) > N:
            raise OverflowError(
                "Число превышает максимальную разрядность N"
            )

    return sign, digits


def to_string(sign, number):
    """Преобразует длинное число в строку.

    Parameters
    ----------
    sign : int
        Знак числа: 1 или -1.
    number : list of int
        Разряды числа в системе с основанием M, от старшего к младшему.

    Returns
    -------
    str
        Разряды через пробел. Старший разряд выводится без ведущих нулей,
        остальные дополнены нулями до WIDTH символов.
        Перед отрицательным числом ставится -.
    """
    body = " ".join(
        [str(number[0])] + [str(d).zfill(WIDTH) for d in number[1:]]
    )

    if sign == -1 and number != [0]:
        return "-" + body

    return body


def compare_abs(a, b):
    """Сравнивает модули двух длинных чисел.

    Parameters
    ----------
    a : list of int
        Разряды первого числа без ведущих нулей.
    b : list of int
        Разряды второго числа без ведущих нулей.

    Returns
    -------
    int
        1, если |a| > |b|; -1, если |a| < |b|;
        0, если модули равны.
    """
    if len(a) > len(b):
        return 1
    if len(a) < len(b):
        return -1
    for i in range(len(a)):
        if a[i] > b[i]:
            return 1
        if a[i] < b[i]:
            return -1
    return 0


def add_abs(a, b):
    """Складывает модули двух длинных чисел.

    Parameters
    ----------
    a : list of int
        Разряды первого слагаемого.
    b : list of int
        Разряды второго слагаемого.

    Returns
    -------
    list of int
        Разряды суммы |a| + |b|.

    Raises
    ------
    OverflowError
        Если в результате больше N разрядов.
    """
    result = []
    carry = 0
    i = len(a) - 1
    j = len(b) - 1

    while i >= 0 or j >= 0 or carry:
        digit_a = a[i] if i >= 0 else 0
        digit_b = b[j] if j >= 0 else 0
        total = digit_a + digit_b + carry
        result.append(total % M)
        carry = total // M
        i -= 1
        j -= 1

    result.reverse()

    if len(result) > N:
        raise OverflowError("Результат превышает максимальную разрядность N")

    return result

 
def subtract_abs(a, b):
    """Вычитает модуль меньшего числа из модуля большего.

    Parameters
    ----------
    a : list of int
        Разряды уменьшаемого, должно выполняться |a| >= |b|.
    b : list of int
        Разряды вычитаемого.

    Returns
    -------
    list of int
        Разряды разности |a| - |b| без ведущих нулей.

    Raises
    ------
    ValueError
        Если |a| < |b|.
    """
    if compare_abs(a, b) < 0:
        raise ValueError("Для этой функции должно выполняться |a| >= |b|")

    result = []
    borrow = 0
    i = len(a) - 1
    j = len(b) - 1

    while i >= 0:
        digit_a = a[i]
        digit_b = b[j] if j >= 0 else 0
        value = digit_a - digit_b - borrow
        if value < 0:
            value += M
            borrow = 1
        else:
            borrow = 0
        result.append(value)
        i -= 1
        j -= 1

    result.reverse()  

    while len(result) > 1 and result[0] == 0:
        result.pop(0)

    return result


def add(sign_a, a, sign_b, b):
    """Складывает два длинных числа со знаками.

    Parameters
    ----------
    sign_a : int
        Знак первого слагаемого: 1 или -1.
    a : list of int
        Разряды первого слагаемого.
    sign_b : int
        Знак второго слагаемого: 1 или -1.
    b : list of int
        Разряды второго слагаемого.

    Returns
    -------
    sign : int
        Знак суммы.
    digits : list of int
        Разряды модуля суммы.

    Raises
    ------
    OverflowError
        Если в результате больше N разрядов.
    """
    if sign_a == sign_b:
        return sign_a, add_abs(a, b)

    cmp = compare_abs(a, b)

    if cmp == 0:
        return 1, [0]

    if cmp > 0:
        return sign_a, subtract_abs(a, b)
    else:
        return sign_b, subtract_abs(b, a)


def subtract(sign_a, a, sign_b, b):
    """Вычитает одно длинное число из другого: a - b.

    Parameters
    ----------
    sign_a : int
        Знак уменьшаемого: 1 или -1.
    a : list of int
        Разряды уменьшаемого.
    sign_b : int
        Знак вычитаемого: 1 или -1.
    b : list of int
        Разряды вычитаемого.

    Returns
    -------
    sign : int
        Знак разности.
    digits : list of int
        Разряды модуля разности.

    Raises
    ------
    OverflowError
        Если в результате больше N разрядов.
    """
    return add(sign_a, a, -sign_b, b)


def multiply(sign_a, a, sign_b, b):
    """Умножает два длинных числа со знаками (умножение в столбик).

    Parameters
    ----------
    sign_a : int
        Знак первого множителя: 1 или -1.
    a : list of int
        Разряды первого множителя.
    sign_b : int
        Знак второго множителя: 1 или -1.
    b : list of int
        Разряды второго множителя.

    Returns
    -------
    sign : int
        Знак произведения. Для нуля всегда 1.
    digits : list of int
        Разряды модуля произведения.

    Raises
    ------
    OverflowError
        Если в результате больше N разрядов.
    """
    if a == [0] or b == [0]:
        return 1, [0]

    result = [0] * (len(a) + len(b))

    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            position = i + j + 1
            result[position] += a[i] * b[j]

    for i in range(len(result) - 1, 0, -1):
        carry = result[i] // M
        result[i] %= M
        result[i - 1] += carry

    while result[0] >= M:
        carry = result[0] // M
        result[0] %= M
        result.insert(0, carry)

    while len(result) > 1 and result[0] == 0:
        result.pop(0)

    if len(result) > N:
        raise OverflowError("Результат превышает максимальную разрядность N")

    return sign_a * sign_b, result


def divide(sign_a, a, sign_b, b):
    """Делит одно длинное число на другое нацело (деление в столбик).

    Частное округляется к нулю: -7 / 2 дает -3.

    Parameters
    ----------
    sign_a : int
        Знак делимого: 1 или -1.
    a : list of int
        Разряды делимого.
    sign_b : int
        Знак делителя: 1 или -1.
    b : list of int
        Разряды делителя.

    Returns
    -------
    sign : int
        Знак частного.
    digits : list of int
        Разряды модуля частного.

    Raises
    ------
    ZeroDivisionError
        Если делитель равен нулю.
    """
    if b == [0]:
        raise ZeroDivisionError("Деление на ноль")

    if compare_abs(a, b) < 0:
        return 1, [0]

    quotient = []
    remainder = [0]

    for digit in a:
        if remainder == [0]:
            remainder = [digit]
        else:
            remainder = remainder + [digit]

        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        q = 0
        for candidate in range(M):
            try:
                product = multiply(1, b, 1, [candidate])[1]
            except OverflowError:
                break

            if compare_abs(product, remainder) <= 0:
                q = candidate
            else:
                break

        quotient.append(q)

        if q != 0:
            product = multiply(1, b, 1, [q])[1]
            remainder = subtract_abs(remainder, product)

    while len(quotient) > 1 and quotient[0] == 0:
        quotient.pop(0)

    return sign_a * sign_b, quotient


def main():
    """Запускает интерактивную демонстрацию длинной арифметики.

    В цикле запрашивает два числа и выводит результаты сложения,
    вычитания, умножения и целочисленного деления. Ввод q завершает
    программу.

    Returns
    -------
    None
    """
    print("Длинная арифметика")
    print(f"Основание M = {M}, разрядность N = {N}")
    print("Вводите целое число, например: 123456789")
    print("Для отрицательных чисел используйте знак '-' в начале.")
    print("Для выхода введите q.")

    while True:
        print()
        numbers = []

        for prompt in ("Введите первое число: ", "Введите второе число: "):
            while True:
                text = input(prompt)

                if text.strip().lower() == "q":
                    print("Выход.")
                    return

                try:
                    numbers.append(from_string(text))
                    break
                except (ValueError, OverflowError) as error:
                    print(f"Ошибка: {error}")

        (sign_a, a), (sign_b, b) = numbers
        str_a = to_string(sign_a, a)
        str_b = to_string(sign_b, b)

        print()
        print("Первое число:", str_a)
        print("Второе число:", str_b)
        print()

        # Сложение
        try:
            sign_r, result = add(sign_a, a, sign_b, b)
            print(f"{str_a} + {str_b} = {to_string(sign_r, result)}")
        except OverflowError as error:
            print(f"Сложение: ошибка — {error}")

        # Вычитание
        try:
            sign_r, result = subtract(sign_a, a, sign_b, b)
            print(f"{str_a} - {str_b} = {to_string(sign_r, result)}")
        except OverflowError as error:
            print(f"Вычитание: ошибка — {error}")

        # Умножение
        try:
            sign_r, result = multiply(sign_a, a, sign_b, b)
            print(f"{str_a} * {str_b} = {to_string(sign_r, result)}")
        except OverflowError as error:
            print(f"Умножение: ошибка — {error}")

        # Деление
        try:
            sign_r, result = divide(sign_a, a, sign_b, b)
            print(f"{str_a} // {str_b} = {to_string(sign_r, result)}")
        except ZeroDivisionError as error:
            print(f"Деление: ошибка — {error}")
        except OverflowError as error:
            print(f"Деление: ошибка — {error}")


if __name__ == "__main__":
    main()
