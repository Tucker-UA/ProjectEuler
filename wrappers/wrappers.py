import time

def printTimeTaken(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"{end-start} seconds")

        return result
    
    return wrapper
