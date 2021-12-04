from . import properties
from . import operators
from . import ui
from . import utils

modules = (
    properties,
    operators,
    ui,
    utils,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()