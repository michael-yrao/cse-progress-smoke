# po-attempt: {"complete": true, "rating": "bogus", "tests": "2/2", "complexity": {"time": "O(n)", "space": "O(1)", "whyTime": "count both", "whySpace": "26 counters"}, "savedAt": "2026-10-19T18:05:00Z"}
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # frequency count
        return sorted(s) == sorted(t)
