import re


"""Utility functions in working with text in Viberary
"""


class InputSanitizer:
    def parse_and_sanitize_input(self, input_string: str) -> str:
        """Sanitize input from search field

        Args:
            input_string (str): input string from search box

        Returns:
            str: cleaned string
        """
        # Remove leading/trailing whitespace
        input_string = input_string.strip()

        # Remove special characters using regex
        input_string = re.sub(r"[^\w\s]", "", input_string)

        # Convert to lowercase
        input_string = input_string.lower()

        # Remove extra whitespaces
        input_string = re.sub(r"\s+", " ", input_string)

        return input_string
