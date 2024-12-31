import unittest
from betterjava.parser import parse_bjava
from betterjava.exceptions import BetterJavaSyntaxError

class TestParser(unittest.TestCase):
    def test_valid_bjava(self):
        code = """
          class HelloWorld:
              main():
                  System.out.println("Hello, world!")
          """
        try:
            parse_bjava(code)
        except BetterJavaSyntaxError:
            self.fail("parse_bjava() raised BetterJavaSyntaxError unexpectedly!")

    def test_missing_colon(self):
        code = """
          class HelloWorld
              main():
                  System.out.println("Hello, world!")
          """
        with self.assertRaises(BetterJavaSyntaxError) as context:
            parse_bjava(code)
        self.assertIn("Missing ':'", str(context.exception))

    def test_unexpected_indentation(self):
        code = """
          class HelloWorld:
                  main():
                      System.out.println("Hello, world!")
          """
        with self.assertRaises(BetterJavaSyntaxError) as context:
            parse_bjava(code)
        self.assertIn("Unexpected indentation", str(context.exception))

if __name__ == "__main__":
    unittest.main()