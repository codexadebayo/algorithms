# write a function to sort for the numbers that appear not more than 2 times in the array 

class Solution():
  def __init__(self) -> None:
    pass

  def solution(self, nums):
    if not nums:
      return 0
    
    def remove_duplicates(index, count):
      if index >= len(nums):
        return count
      
      if index > 0 and nums[index] == nums[index-1]:
        if count < 2:
          nums[count] = nums[index]
          return remove_duplicates(index + 1, count + 1)
        return remove_duplicates(index + 1, count)
      else:
        nums[count] = nums[index]
        return remove_duplicates(index + 1, count + 1)
    
    return remove_duplicates(0, 0)
    
# Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k = k % n  # Handle cases where k > n
        
        # Helper function to reverse array in-place
        def reverse(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
        
        # Step 1: Reverse the entire array
        reverse(0, n-1)
        # Step 2: Reverse the first k elements
        reverse(0, k-1)
        # Step 3: Reverse the remaining elements
        reverse(k, n-1)