import subprocess
import os
import unittest

class TestBjava2JavaIntegration(unittest.TestCase):
    def test_translation_cli(self):

        input_file = "test_input.bjava"
        output_file = "test_output.java"
        with open(input_file, "w") as infile:
            infile.write("""
             class HelloWorld:
                 main():
                     System.out.println("Hello, world!")
             """)

        try:
            # Run the CLI script
            subprocess.run(
                ["bjava2java", input_file, output_file],
                check=True
            )

            with open(output_file, "r") as outfile:
                output_code = outfile.read()

            expected_output = """class HelloWorld {
                 public static void main(String[] args) {
                     System.out.println("Hello, world!");
                 }
             }"""
            self.assertEqual(output_code.strip(), expected_output.strip())
        finally:
            # Clean up files
            os.remove(input_file)
            os.remove(output_file)

if __name__ == "__main__":
    unittest.main()