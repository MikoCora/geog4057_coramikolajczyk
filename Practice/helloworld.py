import arcpy
import os
import sys
class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def add(self, num):
        re = self.real + num.real
        im = self.imag + num.imag
        return ComplexNumber(re, im)

def main():
    """
    This is the main function.
    """

    # Creating complex number instances
    c_1 = ComplexNumber(9, 5)
    print(f"Imaginary part of c_1: {c_1.imag}")

    c_2 = ComplexNumber(1, 8)
    c_3 = c_1.add(c_2)

    print(f"Sum of c_1 and c_2: c_3 = {c_3.real} + {c_3.imag}i")

if __name__ == "__main__":
    main()