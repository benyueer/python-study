from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 1. 两数之和
def twoSum(nums, target):
    map = dict()
    for i, num in enumerate(nums):
        if target - num in map:
            return [map[target-num], i]
        map[num] = i
    return []

    

# 3. 无重复字符的最长子串
def lengthOfLongestSubstring(s):
    map = dict()
    res = 0
    l = 0
    for i, c in enumerate(s):
        l = max(l, map.get(c, 0))
        res = max(res, i - l + 1)
        map[c] = i + 1

    return res


# 5. 最长回文子串
def longestPalindrome(s: str):
    l = len(s)
    dp = [[False] * l for i in range(l)]

    b, e = 0, 0

    for i in range(l).__reversed__():
        for j in range(i,l):
            if i == j:
                dp[i][j] = True
            elif j-i < 2 and s[i] == s[j]:
                dp[i][j] = True
            elif s[i] == s[j] and dp[i+1][j-1]:
                if j - i > e - b:
                    b, e = i, j
                dp[i][j] = True
            else:
                dp[i][j] = False
    return s[b:e+1]


# 2. 两数相加
def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    res = ListNode()
    cur = res
    base = int(0)
    while l1 or l2 or base:
        b1 = l1 and l1.val or 0
        b2 = l2 and l2.val or 0
        t = b1 + b2 + base
        base = int(t / 10)
        cur.next = ListNode(t % 10)
        cur = cur.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return res.next

        