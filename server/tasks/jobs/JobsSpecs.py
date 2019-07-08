#from Sugar import Sugar
from JobsAbstract import JobsAbstract
from JobsException import JobsException
from os import path, getcwd, scandir
import importlib
import sys
import inspect
from importlib import util

class JobsSpecs():
    folder_to_lookup = ''
    handlers = []

    def __init__(self):
        self.folder_to_lookup = path.dirname(path.abspath(__file__))
        sys.path.append(self.folder_to_lookup)
        self.__scan()
        
    def __scan(self):
        files = scandir(self.folder_to_lookup)
        exception_files = ['JobsAbstract.py', 'JobsSpecs.py', '__pycache__', 'JobsException.py']
        self.handlers = [i for i in files if i.name not in exception_files]
        
    def __get_ins(self, file_name:str, file_path:str):
        __ins = None

        try:
            handler_spec = util.spec_from_file_location(file_name, file_path)
            handler_module = util.module_from_spec(handler_spec)
            handler_spec.loader.exec_module(handler_module)
            handler_name = file_name[:-3] #exclusion of .py - need to find a better way
            __class = getattr(handler_module, handler_name)
            __ins = __class()
            if (not isinstance(__ins, JobsAbstract)):
                __ins = None

        except AttributeError:
            pass

        return __ins

    def jobs(self):
        handlers = []
        for i in self.handlers:
            if path.isfile(i.path):
                __ins = self.__get_ins(i.name, i.path)
                if __ins:
                    all_arguments = inspect.getfullargspec(__ins.handle).args[1:]
                    handlers.append({
                        "name": i.name,
                        "arguments": all_arguments
                    })

        return handlers
    
    def handle(self, *, name:str, **kwargs):
        res = None
        path_name = path.join(self.folder_to_lookup, name)
        __ins = self.__get_ins(name, path_name)
        if (__ins):
            res = __ins.handle(**kwargs)
        else:
            print('Seems '+name+' is not a valid job!')
        
        return res

if __name__ == "__main__":
    l =  JobsSpecs()
    l.handle(name='Sugar.py', **{"module":'OP', "json_data": {"d":"d"}})