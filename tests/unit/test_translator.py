import unittest
from betterjava.translator import translate_to_java

class TestTranslator(unittest.TestCase):
    def test_simple_translation(self):
        bjava_code = """
          class HelloWorld:
              main():
                  System.out.println("Hello, world!")
          """
        expected_java = """class HelloWorld {
              public static void main(String[] args) {
                  System.out.println("Hello, world!");
              }
          }"""
        self.assertEqual(translate_to_java(bjava_code), expected_java)

    def test_nested_blocks(self):
        bjava_code = """
          class Example:
              methodA():
                  if (condition):
                      System.out.println("Nested")
          """
        expected_java = """class Example {
              public void methodA() {
                  if (condition) {
                      System.out.println("Nested");
                  }
              }
          }"""
        self.assertEqual(translate_to_java(bjava_code), expected_java)

if __name__ == "__main__":
    unittest.main()