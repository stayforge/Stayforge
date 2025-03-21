"""
Parse user input
"""
import time
from typing import List


def parse_status_codes(rules: List[str]) -> List[int]:
    """
    Parses a list of string rules representing status code ranges or specific codes into a sorted list of integers. The function
    supports inclusion and exclusion rules, where exclusion rules start with '!' and take precedence over inclusions. Ranges are
    specified using a '-' between start and end (e.g., "200-205"). Invalid ranges, empty rules, or invalid numeric formats will
    result in a ValueError being raised. Duplicate codes are automatically handled, ensuring the result contains unique entries.

    :param rules:
        A list of strings where each string represents a rule to define the set of status codes. Inclusion rules specify
        individual codes (e.g., "200") or ranges (e.g., "200-205"). Exclusion rules begin with '!' and specify codes
        or ranges to remove from the inclusion set. For example, "200-205" and "!202-203" would include 200, 201, 204, and 205.
    :return:
        A sorted list of integers representing the final status codes obtained after applying inclusion and exclusion rules.
    """

    str_time = time.time()

    def _expand_range(rule: str) -> List[int]:
        """Expands a single rule string into a list of integers.
        """
        try:
            if "-" in rule:
                start, end = map(int, rule.split("-"))
                if start > end:
                    raise ValueError("Invalid range: start must be less than or equal to end")
                return list(range(start, end + 1))
            else:
                return [int(rule)]
        except ValueError as e:
            raise ValueError(f"Invalid rule: {rule}. {e}") from e  # Chain exceptions for better context

    status_codes = set()
    excluded_codes = set()

    for rule in rules:
        if not rule:  # Handle empty strings
            raise ValueError("Empty rule found")

        if rule.startswith("!"):
            try:
                codes = _expand_range(rule[1:])
                excluded_codes.update(codes)
            except ValueError as e:
                raise ValueError(f"Invalid exclusion rule: {rule}. {e}") from e
        else:
            try:
                codes = _expand_range(rule)
                status_codes.update(codes)
            except ValueError as e:
                raise ValueError(f"Invalid inclusion rule: {rule}. {e}") from e

    # Exclusions take precedence
    final_codes = sorted(status_codes - excluded_codes)
    time.time() - str_time
    return final_codes
