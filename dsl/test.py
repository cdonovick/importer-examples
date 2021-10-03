from type_check import TypeCheckDict

S = '''
x = int
x = 1
x = 'a'
'''
#exec(S, TypeCheckDict(), TypeCheckDict()) # raises TypeError 'a' is not a int

S = '''
def foo():
    x = int
    x = 'a'
foo()
'''

exec(S, TypeCheckDict(), TypeCheckDict()) # raises TypeError 'a' is not a int
