import pytest

from src.aeroplanes import Aeroplane


@pytest.fixture()
def aeroplanes():
    return Aeroplane("United States", "UAL1621", 268.79, 10203.18)


def test_init(aeroplanes):
    """ "Тестирование создания init"""
    assert aeroplanes.country == "United States"
    assert aeroplanes.callsign == "UAL1621"
    assert aeroplanes.velocity == 268.79
    assert aeroplanes.geo_altitude == 10203.18


def test_init_two():
    country = Aeroplane("", "", 268.79, 10203.18)
    assert country.country == "Страна не указана"
    assert country.callsign == "Неизвестен"


def test_validate_country_static():
    """Тестирование статического метода валидации страны"""
    # Вызов статического метода напрямую через класс
    assert Aeroplane._Aeroplane__validate_country("United States") == "United States"


def test_validate_country_empty():
    assert Aeroplane._Aeroplane__validate_country("") == "Страна не указана"
    assert Aeroplane._Aeroplane__validate_country(None) == "Страна не указана"


def test_validate_callsign():
    """Тестирование статического метода валидации позывного"""
    plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    assert plane.callsign == "United States"


def test_validate_callsign_empty():
    assert Aeroplane._Aeroplane__validate_callsign("") == "Неизвестен"
    assert Aeroplane._Aeroplane__validate_callsign(None) == "Неизвестен"


def test_validate_velocity():
    """Проверяет валидацию скорости полета"""

    assert Aeroplane._Aeroplane__validate_velocity("") == 0.0
    assert Aeroplane._Aeroplane__validate_velocity(None) == 0.0
    assert Aeroplane._Aeroplane__validate_velocity(17.6) == 17.6


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", 0.0),
        (None, 0.0),
        (0, 0.0),
        (15.6, 15.6),
    ],
)
def test_validate_geo_altitude(value, expected):
    """Проверяет геометрическую высоту полета"""

    assert Aeroplane._Aeroplane__validate_geo_altitude(value) == expected


def test_cast_to_object_list_valid():
    """Проверяет преобразование корректных данных OpenSky API в список Aeroplane"""
    raw_data = [
        [
            "a1",
            "UAL1621",
            "United States",
            0,
            0,
            0,
            0,
            0,
            False,
            268.79,
            0,
            0,
            None,
            10203.18,
        ],
        ["b2", "AFL123", "Russia", 0, 0, 0, 0, 0, False, 210.5, 0, 0, None, 9500.0],
    ]

    result = Aeroplane.cast_to_object_list(raw_data)

    assert len(result) == 2
    assert isinstance(result[0], Aeroplane)
    assert result[0].country == "United States"
    assert result[0].callsign == "UAL1621"
    assert result[0].velocity == 268.79
    assert result[0].geo_altitude == 10203.18
    assert result[1].country == "Russia"


def test_cast_to_object_list_empty():
    """Проверяет возврат пустого списка при отсутствии данных"""
    assert Aeroplane.cast_to_object_list([]) == []
    assert Aeroplane.cast_to_object_list(None) == []


def test_aeroplane_eq():
    planet = Aeroplane("United States", "UAL1621", 250.0, 10000.0)
    planet2 = Aeroplane("Germany", "DLH400", 250.0, 10000.0)
    planet3 = Aeroplane("Russia", "AFL123", 200.0, 11000.0)

    assert planet == planet2
    assert planet == planet2
    assert planet != planet3


def test_aeroplane_lt_and_gt():
    """Проверяет операторы сравнения < (__lt__) и > (__gt__)"""
    plane_base = Aeroplane("United States", "UAL1621", 250.0, 10000.0)
    plane_higher = Aeroplane("Russia", "AFL123", 200.0, 11000.0)
    plane_faster = Aeroplane("France", "AFR555", 280.0, 10000.0)

    # Сравнение по высоте
    assert plane_base < plane_higher
    assert plane_higher > plane_base

    # Сравнение по скорости при одинаковой высоте
    assert plane_base < plane_faster
    assert plane_faster > plane_base

    with pytest.raises(TypeError):
        _ = plane_base < 10000
    with pytest.raises(TypeError):
        _ = plane_base > "10000"


def test_aeroplane_le_and_ge():
    """Проверяет операторы сравнения"""
    plane_base = Aeroplane("United States", "UAL1621", 250.0, 10000.0)
    plane_equal = Aeroplane("Germany", "DLH400", 250.0, 10000.0)
    plane_higher = Aeroplane("Russia", "AFL123", 200.0, 11000.0)

    # Случай полного равенства параметров
    assert plane_base <= plane_equal
    assert plane_base >= plane_equal

    # Случай строгого неравенства
    assert plane_base <= plane_higher
    assert plane_higher >= plane_base

    # Защита от сравнения с другим типом
    with pytest.raises(TypeError):
        _ = plane_base <= 100
    with pytest.raises(TypeError):
        _ = plane_base >= 100


def test_aeroplane_str():
    """Проверяет строковое представление объекта"""

    plane = Aeroplane("United States", "UAL1621", 268.79, 10203.18)
    expected = (
        "Рейс: UAL1621 | Страна: United States | "
        "Скорость: 268.79 м/с | Высота: 10203.18 м"
    )
    assert str(plane) == expected
