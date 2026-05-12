import pytest
from basic_function_codes.shapes import circle as cr



class TestCircle:

    def setup_method(self, method):

        print(f"\nSetting up for a test: {method.__name__}")

    def test_area(self):
        circle = cr(radius=5)
        assert circle.area() == pytest.approx(78.53981633974483)

    def test_circumference(self):
        circle = cr(radius=5)
        assert circle.circumference() == pytest.approx(31.41592653589793)

    def test_diameter(self):
        circle = cr(radius=5)
        assert circle.diameter() == 10

    def teardown_method(self, method):
        print(f"\nTearing down after test: {method.__name__}")