import main
import unittest


class TestStringFunctions(unittest.TestCase):

    def test_char_diff(self):
        self.assertEqual(main.char_diff('a', 'a'), 0)
        self.assertEqual(main.char_diff('a', 'b'), 1)
        self.assertEqual(main.char_diff('z', 'ź'), 0.5)
        self.assertEqual(main.char_diff('ź', 'ż'), 0.5)
        self.assertEqual(main.char_diff('ć', 'c'), 0.5)

    def test_lev_dist(self):
        self.assertEqual(main.ldist('aba', 'aba'), 0)
        self.assertEqual(main.ldist('kitten', 'sitting'), 3)
        self.assertEqual(main.ldist('test', 'tent'), 1)
        self.assertEqual(main.ldist('book', 'back'), 2)
        self.assertEqual(main.ldist('string', 'truck'), 4)
        self.assertEqual(main.ldist('kampus', 'kampus uj'), 3)
        self.assertEqual(main.ldist('os piastow', 'ospiastow'), 1)
        self.assertEqual(main.ldist('kobierzyńska', 'kobierzyn'), 3.5)

    def test_normalization(self):
        self.assertEqual(main.normalize_name('os.piastow'), 'ospiastow')
        self.assertEqual(main.normalize_name('Kampus UJ'), 'kampus uj')
        self.assertEqual(main.normalize_name('Ruczaj'), 'ruczaj')

if __name__ == '__main__':
    unittest.main()
