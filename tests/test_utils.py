from types import SimpleNamespace

import pytest

from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


@pytest.fixture
def planes():
    return [
        SimpleNamespace(country="Russia", geo_altitude=10000),
        SimpleNamespace(country="USA", geo_altitude=5000),
        SimpleNamespace(country="Germany", geo_altitude=12000),
    ]


@pytest.mark.parametrize(
    "words, expected",
    [
        (["  rUsSiA ", ""], ["Russia"]),
        ([], ["Russia", "USA", "Germany"]),
        (["France"], []),
    ],
)
def test_filter_aeroplanes(planes, words, expected):
    res = filter_aeroplanes(planes, words)
    assert [p.country for p in res] == expected


@pytest.mark.parametrize(
    "alt_range, expected_count, has_error",
    [
        ("5000 - 10000", 2, False),
        ("   ", 3, False),
        ("invalid", 3, True),
    ],
)
def test_get_aeroplanes_by_altitude(
    planes, capsys, alt_range, expected_count, has_error
):
    res = get_aeroplanes_by_altitude(planes, alt_range)
    assert len(res) == expected_count
    assert ("Некорректный формат" in capsys.readouterr().out) == has_error


def test_sort_aeroplanes():

    items = [(5000, 800), (10000, 750), (10000, 900)]
    assert sort_aeroplanes(items) == [(10000, 900), (10000, 750), (5000, 800)]


@pytest.mark.parametrize(
    "top_n, expected_len",
    [
        (2, 2),
        (10, 3),
        (0, 0),
        (-1, 0),
    ],
)
def test_get_top_aeroplanes(planes, top_n, expected_len):
    assert len(get_top_aeroplanes(planes, top_n)) == expected_len


def test_print_aeroplanes(capsys):
    print_aeroplanes([])
    assert "самолеты не найдены" in capsys.readouterr().out

    print_aeroplanes(["Boeing 737"])
    out = capsys.readouterr().out
    assert "1. Boeing 737" in out
    assert "-" * 75 in out
