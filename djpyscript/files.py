import importlib.abc, importlib.util
from importlib.util import spec_from_loader, module_from_spec
import inspect

from django.db.models.fields.files import FieldFile
from contextlib import suppress

from .loaders import StringLoader


class PyScriptFieldFile(FieldFile):
    def import_script(self):
        # Imports the script and returns the module and the module's callable
        spec = spec_from_loader(self.name.split(".")[0], StringLoader(self.file.read()))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module._CALLABLE

    def run_script(self, **injected_parameters):
        # Runs the script and injects the parameters, in case there any from the parameter field
        # As well as the paramters passed in through the injected_keyworks arguments
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
        # Gets the parameters from the script's callable and passes them into the fields parameter field
        # Removes the parameters that are in the injected_paramters list, because they will be added to the script in runtime
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