def mystery_function (x, y):
   x.append (4)
   y = y + 4
   return x, y


a = [1, 2, 3]
b = [1, 2, 3]
result = mystery_function (a, b)
print ("a", a)
print ("b", b)
print ("result", result)