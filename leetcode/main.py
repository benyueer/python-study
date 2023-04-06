# 1. 两数之和
def twoSum(nums, target):
    map = dict()
    for i, num in enumerate(nums):
        if target - num in map:
            return [map[target-num], i]
        map[num] = i
    return []

    

if __name__ == '__main__':
    pass