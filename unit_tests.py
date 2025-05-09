import unittest
import calculations
import translation
import triples

class TestCalculationMethods(unittest.TestCase):
    def setUp(self):
        self.calculations = calculations.Distance()

    def test_distance(self):
        self.assertEqual(self.calculations.distance(point1=[0, 0], point2=[3, 4]), 5, "Invalid result")
        self.assertEqual(self.calculations.distance([0, 0], [5, 12]), 13, "Invalid result")
        self.assertEqual(self.calculations.distance([0, 0], [8, 15]), 17, "Invalid result")
        self.assertEqual(self.calculations.distance([1, 1], [9, 16]), 17, "Invalid result")
        self.assertEqual(self.calculations.gradient([4, 2], [6, 8]), 3, "Invalid result")

    def test_mispoint(self):
        self.assertEqual(self.calculations.midpoint([4, 2], [8, 6]), [6, 4], "Invalid result")
    
    def test_gradient(self):
        self.assertEqual(self.calculations.gradient([4, 2], [6, 8]), 3, "Invalid result")

class TestTranslationMethods(unittest.TestCase):
    def setUp(self):
        self.translations = translation.Translation()

    def test_direction(self):
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 1), [-3, 4], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 2), [-4, 3], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 3), [-4, -3], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 4), [-3, -4], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 5), [3, -4], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 6), [4, -3], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 7), [4, 3], "Invalid result")
        self.assertEqual(self.translations.Triple_to_Movement([3, 4], 8), [3, 4], "Invalid result")

    def test_triple_finder(self):
        self.assertEqual(self.translations.Triple_Finder(5), [3, 4, 5])
        self.assertEqual(self.translations.Triple_Finder(6), [3, 4, 5])
        self.assertEqual(self.translations.Triple_Finder(12), [3, 4, 5])
        self.assertEqual(self.translations.Triple_Finder(13), [5, 12, 13])

    def find_closest_triple(self):
        self.assertEqual(self.translations.Triple_Finder(5, 0), [3, 4, 5], "invalid")
        self.assertEqual(self.translations.Triple_Finder(6, 0), [3, 4, 5])
        self.assertEqual(self.translations.Triple_Finder(12, 0), [3, 4, 5])
        self.assertEqual(self.translations.Triple_Finder(13, 0), [5, 12, 13])


if __name__ == '__main__':
    unittest.main()