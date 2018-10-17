import sys



class LibraryChecker():
    def __init__(self, modules_list):
        self.modules_list = modules_list
        self.loaded_modules = []
        self.name_loaded_modules = []

    def load_modues(self):
        for modules in self.modules_list:
            try:
                #egg_path='C:\\Python36\\eggs\\%s.egg\\' % modules
                egg_path = '//home//egor//eggs//%s.egg' % modules
                print(egg_path)
                sys.path.append(egg_path)
                mod = __import__(modules)
                self.name_loaded_modules.append(modules)
                self.loaded_modules.append(mod)
            except ImportError:
                print("Нет модуля")
        return self.loaded_modules, self.name_loaded_modules



