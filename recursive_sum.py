# A recursive function to add lists 
x = [7,10,68]
def sum(x):
  m = len(x)-1
  if m < 1:
    return x[0]
  y = x[0]
  return y + sum(x[1:])


# x = sum(x)
# print(x)

# Sum items in a list using a loop
def merge_sort(nums1,m, nums2, n):
  ptr1 = m-1
  ptr2 = n-1
  ptr_merged = m + n -1
  while ptr1 >= 0 and ptr2 >=0:
      # compare the last elements
    if nums2[ptr2] > nums1[ptr1]:
      nums1[ptr_merged] = nums2[ptr2]
      ptr2 -= 1
      ptr_merged -=1
    else:
      nums1[ptr_merged] = nums1[ptr1]
      ptr1 -= 1
      ptr_merged -=1

  if ptr2 >= 0:
    nums1[ptr_merged] = nums2[ptr2]
    ptr2 -= 1
    ptr_merged -= 1

  return nums1