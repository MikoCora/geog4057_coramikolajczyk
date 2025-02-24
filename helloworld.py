class ComplexNumber:

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def add(self, num):
        re = self.real + num.real
        im = self.imag + num.imag
        return ComplexNumber(re, im)


def main():

    c_1 = ComplexNumber(2, 1)
    print(c_1.imag)
    c_2 = ComplexNumber(3, 4)
    c_3 = c_1.add(c_2)
    print(f"c_3:{c_3.real}+{c_3.imag}i")
    pass


if __name__ == "__main__":
    main()
