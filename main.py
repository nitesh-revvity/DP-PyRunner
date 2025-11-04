
import os, sys



def set_working_directory():
    """
    Sets working directory to pyrunner's module path
    """
    current_file = sys.modules[__name__].__file__
    pyrunner_path = os.path.dirname(os.path.realpath(current_file))
    os.chdir(pyrunner_path)


if __name__ == '__main__':
    # Need to call this BEFORE importing bootstrapper
    set_working_directory()

    from bootstrap.bootstrap import Bootstrap

    bootstrap = Bootstrap()
    bootstrap.startup()
