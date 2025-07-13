from typing import List


class Solution:

    def kidsWithCandies(
        self, candies: List[int], extraCandies: int
    ) -> List[bool]:

        max_candies = 0
        for candy in candies:
            max_candies = max(candy, max_candies)
            print(max_candies)
        
        return_array = []
        for candy in candies:
            return_array += [(candy + extraCandies >= max_candies)]
        
        return return_array


if __name__ == "__main__":
    # Example usage
    candies = [2, 3, 5, 1, 3]
    extraCandies = 3
    solution = Solution()
    result = solution.kidsWithCandies(candies, extraCandies)
    print(result)
