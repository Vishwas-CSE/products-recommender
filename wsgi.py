import sys
from os import path


def get_abs_path(*paths):
    abs_path = path.abspath( path.join(*paths))
    return abs_path
#
models_module = get_abs_path(__file__, '../app/models/model.py')
print(models_module)
# sys.path.append(models_module)
from app.app import app

if __name__ == "__main__":
    app.run()