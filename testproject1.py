class ComplexNumber:
    """
    This is a class for mathematical operations on complex numbers.
    Attributes:
        real (int): The real part of the complex number.
        imag (int): The imaginary part of the complex number.
    """

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
    c_1 = ComplexNumber(9, 5)
    print(f"Imaginary part of c_1: {c_1.imag}")

    c_2 = ComplexNumber(1, 8)
    c_3 = c_1.add(c_2)

    print(f"Sum of c_1 and c_2: c_3 = {c_3.real} + {c_3.imag}i")

if __name__ == "__main__":
    main()
class Tool:
    def__init__(self):
    """Define the tool parameters."""
    param1 = arcpy.Parameter(
            displayName="Real",
            name="real",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
        )
    param2 = arcpy.Parameter(
            displayName="Imaginary",
            name="imag",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
        )
    param3 = arcpy.Parameter(
            displayName="Real",
            name="real",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
        )
    param4 = arcpy.Parameter(
            displayName="Imaginary",
            name="imag",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
        )        
    params = [param1,param2,param3,param4]