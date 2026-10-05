from collections import Counter

class Solution:

    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        counts = Counter(magazine)

        for char in ransomNote:
            if counts[char] <= 0:
                return False
            counts[char] -= 1

        return True