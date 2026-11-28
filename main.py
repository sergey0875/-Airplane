from src.aeroplanes import Aeroplane
from src.api import APIAdapter
from src.storage import JSONSaver
from src.utils import filter_aeroplanes, get_aeroplanes_by_altitude, sort_aeroplanes, get_top_aeroplanes, \
    print_aeroplanes





def user_interaction():
    """Функция для взаимодействия с пользователем"""
    api = APIAdapter()
    json_saver = JSONSaver()


    country = input("Введите название страны: ").strip()
    raw_aeroplanes = api.get_aeroplanes(country)
    aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)

    if not aeroplanes:
        print(f"Самолеты в воздушном пространстве страны '{country}' не найдены.")
        return

    # Сохраняем все полученные самолеты в JSON-файл
    for plane in aeroplanes:
        json_saver.add_aeroplane(plane)


    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    altitude_range = input("Введите диапазон высот полета (Пример: 5000 - 12000): ")

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)

    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()