import pytest

from src.storage import Aeroplane, JSONSaver


@pytest.fixture
def saver(tmp_path):
    """Создает JSONSaver со временным файлом перед каждым тестом."""
    test_file = tmp_path / "test_aeroplanes.json"
    return JSONSaver(filename=str(test_file))


@pytest.fixture
def sample_plane():
    """Создает тестовый объект самолета."""
    return Aeroplane(
        country="Spain", callsign="IBE123", velocity=850.0, geo_altitude=10500.0
    )


def test_add_and_get_aeroplane(saver, sample_plane):
    """Проверка добавления, защиты от дублей и фильтрации."""
    saver.add_aeroplane(sample_plane)
    saver.add_aeroplane(sample_plane)

    all_planes = saver.get_aeroplanes()
    assert len(all_planes) == 1
    assert all_planes[0]["country"] == "Spain"

    # Проверка фильтрации по критериям
    assert len(saver.get_aeroplanes({"country": "Spain"})) == 1
    assert saver.get_aeroplanes({"country": "USA"}) == []


def test_delete_aeroplane(saver, sample_plane):
    """Проверка удаления самолета."""
    saver.add_aeroplane(sample_plane)
    saver.delete_aeroplane(sample_plane)

    assert saver.get_aeroplanes() == []


def test_invalid_type_raises_error(saver):
    """Проверка выброса ошибки при передаче не объекта Aeroplane."""
    with pytest.raises(TypeError):
        saver.add_aeroplane("не самолет")

    with pytest.raises(TypeError):
        saver.delete_aeroplane({"country": "Spain"})
