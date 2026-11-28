from src.aeroplanes import Aeroplane


def filter_aeroplanes(
    aeroplanes: list[Aeroplane], filter_words: list[str]
) -> list[Aeroplane]:
    """Фильтрует самолеты по названиям стран регистрации."""
    if not filter_words:
        return aeroplanes

    normalized_words = [word.strip().lower() for word in filter_words if word.strip()]
    return [plane for plane in aeroplanes if plane.country.lower() in normalized_words]


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    """Фильтрует самолеты по диапазону высот."""
    if not altitude_range.strip():
        return aeroplanes

    try:
        parts = altitude_range.replace(" ", "").split("-")
        if len(parts) != 2:
            raise ValueError
        min_alt, max_alt = float(parts[0]), float(parts[1])
        return [
            plane for plane in aeroplanes if min_alt <= plane.geo_altitude <= max_alt
        ]
    except ValueError:
        print("Некорректный формат диапазона высот. Фильтр по высоте пропущен.")
        return aeroplanes


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолеты по убыванию высоты полета и скорости."""
    return sorted(aeroplanes, reverse=True)


def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Возвращает топ N самолетов из списка."""
    if top_n <= 0:
        return []
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Красиво выводит список самолетов в консоль."""
    if not aeroplanes:
        print("По вашему запросу самолеты не найдены.")
        return

    print("-" * 75)
    for index, plane in enumerate(aeroplanes, start=1):
        print(f"{index}. {plane}")
    print("-" * 75)
