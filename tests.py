import sys
sys.path.insert(0, '..')
from evilshortgen import shortgen
import unittest


class TestDecorator(unittest.TestCase):
    def test_decorator(self):
        @shortgen
        def test():
            a << sum([1, 2, 3])
            self.assertEqual(a, 5)
            b = 1
            b << 2
            self.assertEqual(b, 7)
            c << sum([
                1, 2,
            ])
            self.assertEqual(c, 8)
        gen = test()
        self.assertEqual(6, gen.send(None))
        self.assertEqual(2, gen.send(5))
        self.assertEqual(3, gen.send(7))
        with self.assertRaises(StopIteration):
            gen.send(8)


if __name__ == '__main__':
    unittest.main()
