import pytest
from triangle_class import Triangle, IncorrectTriangleSides


# Позитивные тесты
def test_equilateral():
    t = Triangle(3, 3, 3)
    assert t.triangle_type() == "equilateral"
    assert t.perimeter() == 9


def test_isosceles():
    t = Triangle(5, 5, 3)
    assert t.triangle_type() == "isosceles"


def test_nonequilateral():
    t = Triangle(4, 5, 6)
    assert t.triangle_type() == "nonequilateral"


# Негативные тесты
def test_invalid_zero():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 1, 1)


def test_invalid_negative():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 2, 3)


def test_invalid_triangle():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 3)


def test_invalid_type():
    with pytest.raises(IncorrectTriangleSides):
        Triangle("a", 2, 3)