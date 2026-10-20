def contains_duplicate(nums):
    seen = set()
    for i in range(len(nums) - 1):
        if nums[i] in seen:
            return True
        seen.add(nums[i])
    return False
