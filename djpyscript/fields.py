import importlib.abc, importlib.util
from importlib.util import spec_from_loader, module_from_spec
import inspect
from django.db.models import FileField
from django.db.models.fields.files import FieldFile
from contextlib import suppress

class StringLoader(importlib.abc.SourceLoader):
    def __init__(self, data):
        self.data = data

    def get_source(self, fullname):
        return self.data

    def get_source(self, fullname):
        return self.data
    
    def get_data(self, path):
        return self.data
    
    def get_filename(self, fullname):
        return "<not a real path>/" + fullname + ".py"


class PyScriptFieldFile(FieldFile):
    def import_script(self):
        spec = spec_from_loader(self.name.split(".")[0], StringLoader(self.file.read()))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module._CALLABLE

    def run_script(self, **injected_parameters):
        """ Throws TypeError if not all mandatory parameters are inserted """
        module, method = self.import_script()

        if self.field.parameter_field:
            injected_parameters.update(getattr(self.instance, self.field.parameter_field))

        return method(**injected_parameters)

    def cast_parameters(self, signature):
        parameters = getattr(self.instance, self.field.parameter_field)

        for parameter_key, parameter in signature.parameters.items():
            if parameter.annotation:
                parameters[parameter_key] = parameter.annotation(parameters[parameter_key])
        return parameters

    def get_parameters(self):
        signature = inspect.signature(self.import_script()[1])
        parameters = signature.parameters

        parameter_field = getattr(self.instance, self.field.parameter_field)
        keys = list(parameter_field.keys())

        if parameter_field is None:
            parameter_field = {}

        filtered_parameters = filter(lambda p: p[0] not in self.field.injected_parameters, parameters.items())
        for parameter_key, parameter in filtered_parameters:

            with suppress(ValueError):
                keys.remove(parameter_key)

            default = "" if parameter.default == inspect.Parameter.empty else parameter.default
            parameter_field.setdefault(parameter.name, str(default))

        for key in keys:
            del parameter_field[key]

        return parameter_field


class PyScriptField(FileField):
    attr_class = PyScriptFieldFile

    def __init__(self, injected_parameters=[], parameter_field=None, *args, **kwargs):
        self.parameter_field = parameter_field
        self.injected_parameters = injected_parameters
        super().__init__(*args, **kwargs)
