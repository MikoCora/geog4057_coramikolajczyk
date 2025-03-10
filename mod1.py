import importlib
import mod1
importlib.reload(mod1)


s = "Some strings here"
a = [100, 200, 300]


def foo(arg):
    print(f'arg = {arg}')


class Foo:
    def __str__(self):
        return "Instance of Foo"


List = ["GIS", "Programming", "Class"]
print("\nList containing multiple values: ")
print(List)


# Creating a Multi-Dimensional List
# (By Nesting a list inside a List)
List2 = [['GIS', 'Programming'], ['Class']]
print("\nMulti-Dimensional List: ")
print(List2)


# accessing a element from the
# list using index numbe
print("Accessing element from the list")
print(List[0])
print(List[2])


# accessing a element using
# negative indexing
print("Accessing element using negative indexing")
print(List[-1])
print(List[-2])
print(List[-3])
