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
    
