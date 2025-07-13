import logging
import sys


class Solution:
    logger = logging.getLogger()

    def __init__(self):
        self.logger.name = "gcdOfStrings"
        self.logger.addHandler(logging.StreamHandler(stream=sys.stderr))
        self.logger.setLevel("DEBUG")

    def runTests(self) -> tuple[int, int, int]:
        """
        Runs a series of test cases for the `gcdOfStrings` method, printing the results for each case.
        The test cases cover various scenarios, including:
            - Both strings are non-empty and have a common divisor.
            - One string is empty.
            - Both strings are empty.
            - Strings with no common divisor.
            - Strings of different lengths.
        Returns:
            (n_tests, n_pass, n_fail): total number of tests that were run, the number of tests that passed, and the number of tests that failed.
        """

        tests = {
            "test_01a": {
                "str1": "ABCABC",
                "str2": "ABC",
                "expected_result": "ABC",
                "description": "match with longer first string",
            },
            "test_01b": {
                "str1": "ABC",
                "str2": "ABCABC",
                "expected_result": "ABC",
                "description": "match with longer second string",
            },
            "test_02a": {
                "str1": "ABCABC",
                "str2": "ABCABC",
                "expected_result": "ABCABC",
                "description": "matching a repetitive block, whole word",
            },
            "test_02b": {
                "str1": "ABABABAB",
                "str2": "ABAB",
                "expected_result": "AB",
                "description": "matching a repetitive block, partial word",
            },
            "test_03a": {
                "str1": "",
                "str2": "ABC",
                "expected_result": "",
                "description": "first string is empty",
            },
            "test_03b": {
                "str1": "ABC",
                "str2": "",
                "expected_result": "",
                "description": "second string is empty",
            },
            "test_03c": {
                "str1": "ABCABC",
                "str2": "",
                "expected_result": "",
                "description": "both strings are empty",
            },
            "test_04a": {
                "str1": "ABCABC",
                "str2": "ABCD",
                "expected_result": "",
                "description": "no match - extra letter at end of str2",
            },
            "test_04b": {
                "str1": "ABCABC",
                "str2": "ABCABEC",
                "expected_result": "",
                "description": "no match - extra letter in middle of str2",
            },
            "test_04c": {
                "str1": "LEET",
                "str2": "HACK",
                "expected_result": "",
                "description": "no match - no letters in common",
            },
            "test_05a": {
                "str1": "INTENTIONAL",
                "str2": "FAILURE",
                "expected_result": "XYZ",
                "description": "intentional test failure",
            },
        }
        n_tests = len(tests)
        n_pass = n_fail = 0

        for test_name, test_data in tests.items():
            result = self.gcdOfStrings(test_data["str1"], test_data["str2"])
            if result == test_data["expected_result"]:
                n_pass += 1
                print(
                    f"Test {test_name} succeeded and returned '{result}', as expected [{test_data["description"]}]."
                )
            else:
                n_fail += 1
                print(
                    f"Test {test_name} failed. It returned '{result}' but the expected value was '{test_data["expected_result"]}' [{test_data["description"]}]."
                )

        return (n_tests, n_pass, n_fail)

    def gcdOfStrings(self, str1: str, str2: str) -> str:
        """
        Finds the greatest common divisor string of two input strings.

        Parameters:
            str1 (str): The first input string.
            str2 (str): The second input string.

        Returns:
            str: The greatest common divisor string of str1 and str2, or an appropriate value if none exists.

        **Known constraints:**
            1 <= len(str1), len(str2) <= 1000
            All letters are English and upper-case
        """

        # swap strings if needed so that str1 is always the longest one:
        if len(str2) > len(str1):
            _ = str1
            str1 = str2
            str2 = _

        try:
            candidate = ""
            match = True
            i = 0

            # interate over the shorter string, as it's the longest possible match:
            while i < len(str2) and match:
                if str1[i] == str2[i]:
                    candidate += str1[i]
                else:
                    match = False

                i += 1

            for s in str1, str2:
                multiple = int(len(s) / len(candidate))

                if not multiple.is_integer():
                    candidate = ""
                elif not candidate * multiple == s:
                    candidate = ""

        except Exception:
            candidate = ""

        return candidate


if __name__ == "__main__":
    s = Solution()
    n_tests, n_pass, n_fail = s.runTests()
    print(
        f"\nSummary: {n_tests} tests executed; {n_pass} succeeded and {n_fail} failed.\n"
    )
