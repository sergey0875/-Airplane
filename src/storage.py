import json
import os
from abc import ABC, abstractmethod
from typing import Any

from src.aeroplanes import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс-коннектор для работы с хранилищем данных о самолетах."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолете в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Получает данные из хранилища по указанным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолете из хранилища."""
        pass


class JSONSaver(BaseStorage):
    """Класс для сохранения, чтения и удаления данных о самолетах в JSON-файле."""

    def __init__(
        self,
        filename: str = "C:/Users/sepaa/PycharmProjects/Project 2. Aircraft Tracker/data/aeroplanes.json",
    ) -> None:
        self.__filename = filename
        self.__ensure_file_exists()

    def __ensure_file_exists(self) -> None:
        """Создает директорию и пустой JSON-файл, если они еще не существуют."""
        directory = os.path.dirname(self.__filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.__filename):
            self.__write_data([])

    def __read_data(self) -> list[dict[str, Any]]:
        """Считывает весь список самолетов из JSON-файла."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def __write_data(self, data: list[dict[str, Any]]) -> None:
        """Перезаписывает JSON-файл обновленным списком данных."""
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def __aeroplane_to_dict(aeroplane: Aeroplane) -> dict[str, Any]:
        """Преобразует объект Aeroplane в словарь для сериализации в JSON."""
        return {
            "country": aeroplane.country,
            "callsign": aeroplane.callsign,
            "velocity": aeroplane.velocity,
            "geo_altitude": aeroplane.geo_altitude,
        }

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в JSON-файл, избегая дублирования."""
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Ожидается объект класса Aeroplane")

        data = self.__read_data()
        plane_dict = self.__aeroplane_to_dict(aeroplane)

        if plane_dict not in data:
            data.append(plane_dict)
            self.__write_data(data)

    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Возвращает список самолетов из файла.
        Если передан словарь criteria (например, {'country': 'Spain'}), фильтрует по нему.
        """
        data = self.__read_data()
        if not criteria:
            return data

        filtered_data = []
        for item in data:
            if all(item.get(key) == value for key, value in criteria.items()):
                filtered_data.append(item)
        return filtered_data

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет конкретный самолет из JSON-файла."""
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Ожидается объект класса Aeroplane")

        data = self.__read_data()
        plane_dict = self.__aeroplane_to_dict(aeroplane)
        updated_data = [item for item in data if item != plane_dict]

        if len(updated_data) != len(data):
            self.__write_data(updated_data)
