def check_unique_digits(digits):
  """
  Checks if all digits (0-9) are unique in a given integer.

  Args:
      digits: The integer to check for unique digits.

  Returns:
      True if all digits are unique, False otherwise.
  """
  digits.split(',')
  #print (digits)
  arr = []
  for cr in digits:
      if cr in arr:
        return False
      arr.append(cr)
  return True

def find_solutions():
  """
  Finds integers where two products (gor2, gbis2) satisfy certain conditions
  with unique digits (0-9).

  Prints solutions in the specified format if found.
  """
  for d in range(10):
    for g in range(10):
      for l in range(10):
        for s in range(10):
          for r in range(10):
            for b in range(10):
              for o in range(10):
                for y in range(10):
                  if check_unique_digits(f"{d},{g},{l},{s},{o},{b},{r},{y}"):  # Combined string for efficiency
                    print ("unic")
                    gorT = int(f'{r}{o}{g}')
                    gor2 = int(f'{l}{g}{d}') * int(f'{l}{g}{d}')
                    gbisT = int(f'{s}{y}{b}{g}')
                    gbis2 = int(f'{g}{b}{l}') + gorT
                    if gor2 == gorT or gbis2 == gbisT:
                      print(f"the answer is: {gorT} \n")
            

# # Call the find_solutions function to find potential answers
# # find_solutions()
# for g in range(10):
#     for o in range(10):
#         for r in range(10):
#             for l in range(10):
#                 for d in range(10):
#                     gorT = int(f'{r}{o}{g}')
#                     gor2 = int(f'{l}{g}{d}') * int(f'{l}{g}{d}')
#                     if gor2 == gorT:
#                         print(gorT) 361
            