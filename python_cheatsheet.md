# Python Cheat Sheet (2025 Edition)  
One-page reference for daily coding – print it or keep open!

### 1. Basics & Syntax
```python
# Comments
# Single line    |  """ Multi-line """

# Variables (dynamic typing)
name = "Alice"
age = 25
height = 5.8
is_student = True

# Print & f-strings (Python 3.6+)
print(f"Hello {name}, you are {age} years old")

# Input
age = int(input("Enter age: "))

# Type conversion
int(), float(), str(), bool(), list(), tuple(), set(), dict()
```

### 2. Data Types Quick Look
| Type       | Mutable? | Example                          |
|------------|----------|----------------------------------|
| int        | -        | 42                               |
| float      | -        | 3.14                             |
| str        | No       | "hello" or 'hello' or """multi"""|
| bool       | -        | True / False                     |
| list       | Yes      | [1, 2, 3]                        |
| tuple      | No       | (1, 2, 3)                        |
| set        | Yes      | {1, 2, 3}                        |
| frozenset  | No       | frozenset([1,2,3])               |
| dict       | Yes      | {"name": "Bob", "age": 30}       |

### 3. Operators
```python
# Arithmetic
+  -  *  /  //  % 2**10   # 1024

# Comparison
==  !=  >  <  >=  <=  is  is not

# Logical
and  or  not

# Membership & Identity
x in lst        x not in lst
x is None       x is not None
```

### 4. Strings
```python
s = "  Python is awesome  "

s.upper()           # "PYTHON IS AWESOME"
s.lower()           # "python is awesome"
s.strip()           # "Python is awesome"
s.replace("a", "@")
s.split()           # ['Python', 'is', 'awesome']
" ".join(['a','b']) # "a b"
f"Hello {name.upper()}"

# Slicing: s[start:stop:step]
s[::2]              # every 2nd char
s[::-1]             # reverse string
```

### 6. Lists
```python
lst = [10, 20, 30, 40]

lst.append(50)
lst.extend([60,70])
lst.insert(0, 5)
lst.remove(20)            # by value
lst.pop()                 # last item (or pop(index))
lst.clear()

# List comprehension
[x**2 for x in range(10) if x%2==0]
```

### 7. Tuples, Sets, Dicts
```python
# Tuple (immutable)
t = (1, 2, 3)

# Set (unique, unordered)
s = {1, 2, 3}
s.add(4)
s.discard(2)              # safe remove
a | b                     # union
a & b                     # intersection

# Dict
d = {"name": "Alice", "age": 25}
d["city"] = "Delhi"
d.get("age", "N/A")      # safe get
d.keys(), d.values(), d.items()
d.pop("age")
```

### 8. Control Flow
```python
# if-elif-else
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary
status = "adult" if age >= 18 else "minor"

# for loop
for i in range(5):               # 0 to 4
for idx, val in enumerate(lst):
for k, v in d.items():

# while
while x > 0:
    x -= 1
else:                            # runs if no break
    print("done")
```

### 9. Functions
```python
def greet(name="World", greet="Hi"):
    return f"{greet} {name}!"

# *args, **kwargs
def func(*args, **kwargs):
    print(args)      # tuple
    print(kwargs)    # dict

# Lambda
square = lambda x: x*x
```

### 10. Exception Handling
```python
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print(e)
except Exception as e:
    print("Something else")
else:
    print("No error")
finally:
    print("Always runs")
```

### 11. OOP Quick
```python
class Person:
    species = "Homo sapiens"                # class variable

    def __init__(self, name, age):
        self.name = name                     # instance variable
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.age})"

    @property
    def is_adult(self):
        return self.age >= 18

    @staticmethod
    def is_weekend(day):
        return day in ["Sat", "Sun"]
```

### 12. Common Built-in Functions
```python
len(), type(), id(), print(), input()
range(), enumerate(), zip()
map(), filter(), sorted(), reversed()
any(), all(), max(), min(), sum()
open("file.txt", "r") as f: ...
```

### 13. File Handling
```python
# Text
with open("file.txt", "w") as f:
    f.write("hello\n")

with open("file.txt", "r") as f:
    content = f.read()
    lines = f.readlines()

# JSON
import json
json.dump(data, f)
data = json.load(f)

# CSV
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader: ...
```

### 14. Useful One-liners
```python
# Swap variables
a, b = b, a

# Flatten list of lists
flat = [item for sub in lst for item in sub]

# Read entire file
open("f.txt").read()

# Reverse string/list
s[::-1]

# Count occurrences
lst.count(x)  or  from collections import Counter
```

### 15. Virtual Environment & Packages
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install requests pandas
pip freeze > requirements.txt
```

Keep this cheat sheet in your editor or print it — it covers 95% of daily Python needs!  
Happy coding! 🚀
