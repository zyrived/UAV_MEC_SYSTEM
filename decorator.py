# 定义一个装饰器函数
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)  # 调用被装饰的函数并传递参数
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")

@my_decorator
def calculate(a, b):
    result = a + b
    print(f"The result is: {result}")

# 调用被装饰的函数，传递不同数量的参数
greet("Alice")
calculate(5, 3)


