import unittest


class TestControlFlow(unittest.TestCase):

    def test_if(self):
        x = int(input("input a number:"))
        if x < 0:
            x = 0
            print("less than 0")
        elif x == 0:
            print("equal 0")
        elif x > 0:
            print("more than 0")

    def test_for(self):
        words = [12, 'qwe']
        for w in words:
            print(w)
