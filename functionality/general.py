from functools import lru_cache


@lru_cache(None)
def isSubString(abbreviation: str, full_word: str) -> tuple[bool, int]:
    abbreviation = abbreviation.lower()

    if abbreviation[0] != full_word[0]:
        return False, 0

    full_word = full_word

    m = len(abbreviation)
    if m == 0:
        return True, 0

    n = len(full_word)

    abbr_index = 0
    full_index = 0

    while abbr_index < m and full_index < n:
        if abbreviation[abbr_index] == full_word[full_index]:
            abbr_index += 1
        full_index += 1

    if m > 3:
        return abbr_index > (m - 2), abbr_index
    return abbr_index == m, abbr_index
