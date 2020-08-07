# -*- coding: utf-8 -*-
import pkgutil
import importlib
import inspect

import pkg_resources

from mcomix.log import __logger, DEBUG
import mcomix.plugins.base

__logger.setLevel(DEBUG)
log = __logger.getChild(__package__)


def _get_entrypoints():
    for plugin in pkg_resources.iter_entry_points('mcomix.plugins'):
        yield plugin


def _entrypoint_load_plugin(plugin, error=False):
    try:
        obj = plugin.load()
    except ImportError:
        log.error("Unable to load plugin from entrypoint `{}`".format(plugin))
        if error:
            raise
        return None

    # Make sure this is a plugin
    if not issubclass(obj, mcomix.plugins.base.BasePlugin):
        log.error("{}.{} is not a subclass of BasePlugin (found via entrypoint)".format(obj.__module__, obj.__name__))
        if error:
            raise TypeError("Class {} is not a plugin.".format(obj))
        return None

    return obj


def get_entrypoint_plugins():
    "Returns an iterable containing all plugins found via the `mcomix.plugins` entrypoint."
    plugins = set()

    # Iterate over plugin entrypoints
    for plugin in _get_entrypoints():
        obj = _entrypoint_load_plugin(plugin)

        if obj is not None:
            plugins.add(obj)
            log.info("Found plugin {} at {}.{} via entrypoint ({})".format(obj.name, obj.__module__, obj.__name__, plugin.name))

    return plugins


def get_module_plugins():
    "Returns an iterable containing all plugin classes found in the `mcomix.plugins` module."
    plugins = set()

    # Iterate over submodules of mcomix.plugins
    for finder, name, ispkg in pkgutil.iter_modules(__path__, __package__ + "."):
        plugin_module = importlib.import_module(name)

        # Skip classes from mcomix.plugins.base
        if plugin_module is mcomix.plugins.base:
            continue

        # Iterate over classes in module
        for obj_name, obj in inspect.getmembers(plugin_module, inspect.isclass):
            # Make sure this is a plugin
            if not issubclass(obj, mcomix.plugins.base.BasePlugin):
                log.debug("{}.{} is not a subclass of BasePlugin".format(name, obj.__name__))
                continue

            # Make sure class is defined in this module or a submodule
            if inspect.getmodule(obj) is plugin_module or obj.__module__.startswith(name + '.'):

                plugins.add(obj)
                log.info("Found plugin {} at {}.{} via pkgutil".format(obj.name, name, obj_name))

    return plugins


def get_plugins():
    "Returns an iterable containing all known plugin classes."
    plugins = set()

    plugins.update(get_entrypoint_plugins())
    plugins.update(get_module_plugins())

    return plugins


__all__ = [
    "get_plugins",
    "get_entrypoint_plugins",
    "get_module_plugins",
]
