from typing import List


class Solution:

    def kidsWithCandies(
        self, candies: List[int], extraCandies: int) -> List[bool]:
        current_max = max(candies)
        return [
            c + extraCandies >= current_max
            for c in candies
        ]

if __name__ == "__main__":
    # Example usage
    candies = [2, 3, 5, 1, 3]
    extraCandies = 3
    solution = Solution()
    result = solution.kidsWithCandies(candies, extraCandies)
    print(result)
