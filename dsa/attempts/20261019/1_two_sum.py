# po-attempt: {"complete": true, "rating": "clean", "tests": "3/3", "complexity": {"time": "O(n)", "space": "O(n)", "whyTime": "one pass over nums", "whySpace": "hash map of seen values"}, "savedAt": "2026-10-19T18:00:00Z"}
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # complement lookup in a hash map
        seen = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i
