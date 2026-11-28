from unittest.mock import Mock, patch

from src.api import APIAdapter


@patch("src.api.get")
def test_get_aeroplanes_success(mock_get):
    """Проверяет успешное получение списка самолётов по стране"""

    mock_nominatim_response = Mock()
    mock_nominatim_response.json.return_value = [
        {"boundingbox": ["35.2889", "47.0921", "6.6272", "18.7844"]}
    ]


    sample_states = [
        [
            "300aa9",
            "IRBNS   ",
            "Italy",
            1795856586,
            1795856586,
            10.3554,
            45.5739,
            731.52,
            False,
            32.74,
            45,
            3.9,
            None,
            876.3,
            None,
            False,
            0,
        ],
        [
            "300ab0",
            "ITY640  ",
            "Italy",
            1795856587,
            1795856587,
            12.151,
            41.8358,
            632.46,
            False,
            130.16,
            269.32,
            5.85,
            None,
            723.9,
            "1262",
            False,
            0,
        ],
    ]
    mock_opensky_response = Mock()
    mock_opensky_response.json.return_value = {
        "time": 1795856587,
        "states": sample_states,
    }

    # Связываем оба ответа по очереди через side_effect
    mock_get.side_effect = [mock_nominatim_response, mock_opensky_response]

    # Вызываем тестируемый метод
    adapter = APIAdapter()
    result = adapter.get_aeroplanes("Italy")

    # Проверяем результат, обновление атрибута и вызовы get()
    assert result == sample_states
    assert adapter.aeroplanes == sample_states
    assert mock_get.call_count == 2

    # Проверяем параметры первого запроса (Nominatim)
    first_call_kwargs = mock_get.call_args_list[0].kwargs
    assert first_call_kwargs["url"] == "https://nominatim.openstreetmap.org/search"
    assert first_call_kwargs["params"] == {
        "country": "Italy",
        "format": "json",
        "limit": 1,
    }
    assert first_call_kwargs["headers"] == {"User-Agent": "test-app/1.0"}

    # Проверяем параметры второго запроса (OpenSky)
    second_call_kwargs = mock_get.call_args_list[1].kwargs
    assert second_call_kwargs["url"] == "https://opensky-network.org/api/states/all?"
    assert second_call_kwargs["params"] == {
        "lamin": "35.2889",
        "lamax": "47.0921",
        "lomin": "6.6272",
        "lomax": "18.7844",
    }


@patch("src.api.get")
def test_get_aeroplanes_empty_states(mock_get):
    """Проверяет возврат пустого списка, если в ответе OpenSky нет ключа states"""
    mock_nominatim_response = Mock()
    mock_nominatim_response.json.return_value = [
        {"boundingbox": ["35.2889", "47.0921", "6.6272", "18.7844"]}
    ]

    mock_opensky_response = Mock()
    mock_opensky_response.json.return_value = {"time": 1795856587}

    mock_get.side_effect = [mock_nominatim_response, mock_opensky_response]

    adapter = APIAdapter()
    result = adapter.get_aeroplanes("Italy")

    assert result == []
    assert adapter.aeroplanes == []
