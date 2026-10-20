"""
1. Two Sum   ·   https://progressiveoverflow.com/practice/1
Pattern: arrays_and_hash
Difficulty: Easy
"""

class Solution:

    # ── Attempt · 2026-10-19 ──────────────
    def twoSum_20261019(self, nums: List[int], target: int) -> List[int]:
        # complement lookup in a hash map
        seen = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i
