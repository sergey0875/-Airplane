from typing import Any


class Aeroplane:

    def __init__(self, country, callsign, velocity, geo_altitude):
        self.__country = self.__validate_country(country, "Страна не указана")
        self.__callsign = self.__validate_callsign(callsign, "Неизвестен")
        self.__velocity = self.__validate_velocity(velocity)
        self.__geo_altitude = self.__validate_geo_altitude(geo_altitude)

    @staticmethod
    def __validate_country(country: Any, default: str = "Страна не указана") -> str:
        """Проверяет название страны регистрации."""
        if isinstance(country, str) and country.strip():
            return country.strip()
        return default

    @staticmethod
    def __validate_callsign(callsign: Any, default: str = "Неизвестен") -> str:
        """Проверяет позывной самолета и убирает лишние пробелы."""
        if isinstance(callsign, str) and callsign.strip():
            return callsign.strip()
        return default

    @staticmethod
    def __validate_velocity(velocity: Any) -> float:
        """Проверяет скорость полета (м/с). Если пришел None или отрицательное число, возвращает 0.0."""
        if (
            isinstance(velocity, (int, float))
            and not isinstance(velocity, bool)
            and velocity >= 0
        ):
            return float(velocity)
        return 0.0

    @staticmethod
    def __validate_geo_altitude(geo_altitude: Any) -> float:
        """Проверяет геометрическую высоту полета (м). Если пришел None, возвращает 0.0."""
        if (
            isinstance(geo_altitude, (int, float))
            and not isinstance(geo_altitude, bool)
            and geo_altitude >= 0
        ):
            return float(geo_altitude)
        return 0.0

        # Геттеры (инкапсуляция)

    @property
    def country(self) -> str:
        return self.__country

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def geo_altitude(self) -> float:
        return self.__geo_altitude

    @classmethod
    def cast_to_object_list(cls, aeroplanes_data: list[list[Any]]) -> list["Aeroplane"]:
        """Преобразует сырой ответ OpenSky API в список объектов Aeroplane."""

        if not aeroplanes_data:
            return []

        aeroplanes = []
        for item in aeroplanes_data:
            if len(item) < 14:
                continue
            aeroplanes.append(
                cls(
                    country=item[2],
                    callsign=item[1],
                    velocity=item[9],
                    geo_altitude=item[13],
                )
            )
        return aeroplanes

    # Сравнение самолетов по высоте и скорости
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__geo_altitude, self.__velocity) == (
            other.__geo_altitude,
            other.__velocity,
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__geo_altitude, self.__velocity) < (
            other.__geo_altitude,
            other.__velocity,
        )

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__geo_altitude, self.__velocity) <= (
            other.__geo_altitude,
            other.__velocity,
        )

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__geo_altitude, self.__velocity) > (
            other.__geo_altitude,
            other.__velocity,
        )

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__geo_altitude, self.__velocity) >= (
            other.__geo_altitude,
            other.__velocity,
        )

    def __str__(self) -> str:
        return (
            f"Рейс: {self.__callsign} | Страна: {self.__country} | "
            f"Скорость: {self.__velocity} м/с | Высота: {self.__geo_altitude} м"
        )
