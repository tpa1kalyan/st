# Program to check type of triangle (with max input = 10)

# Take input from user
a = int(input("Enter side a (max 10): "))
b = int(input("Enter side b (max 10): "))
c = int(input("Enter side c (max 10): "))

# Check if inputs are in valid range
if a <= 0 or b <= 0 or c <= 0 or a > 10 or b > 10 or c > 10:
    print("Out of range values")
else:
    # Check triangle inequality
    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            print("Equilateral triangle")
        elif a == b or b == c or a == c:
            print("Isosceles triangle")
        else:
            print("Scalene triangle")
    else:
        print("Triangle cannot be formed")