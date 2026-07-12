import sys

def test_environment():
    print(f"Running tests in: {sys.prefix}")
    # A simple dummy test
    assert True

if __name__ == '__main__':
    test_environment()
    print("Tests passed!")
