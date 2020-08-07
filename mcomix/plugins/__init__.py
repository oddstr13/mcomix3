# -*- coding: utf-8 -*-
import pkgutil
import importlib
import inspect

import pkg_resources

from mcomix.log import __logger, DEBUG
import mcomix.plugins.base

__logger.setLevel(DEBUG)
log = __logger.getChild(__package__)


def get_plugins():
    plugins = []

    for plugin in pkg_resources.iter_entry_points('mcomix.plugins'):
        try:
            obj = plugin.load()
        except ImportError:
            log.error("Unable to load plugin from entrypoint `{}`".format(plugin))
            continue

        # Make sure this is a plugin
        if not issubclass(obj, mcomix.plugins.base.BasePlugin):
            log.error("{}.{} is not a subclass of BasePlugin (found via entrypoint)".format(obj.__module__, obj.__name__))
            continue
        plugins.append(obj)
        log.info("Found plugin {} at {}.{} via entrypoint ({})".format(obj.name, obj.__module__, obj.__name__, plugin.name))

    for finder, name, ispkg in pkgutil.iter_modules(__path__, __package__ + "."):
        plugin_module = importlib.import_module(name)

        # Skip classes from mcomix.plugins.base
        if plugin_module is mcomix.plugins.base:
            continue

        for obj_name, obj in inspect.getmembers(plugin_module, inspect.isclass):
            # Make sure this is a plugin
            if not issubclass(obj, mcomix.plugins.base.BasePlugin):
                log.debug("{}.{} is not a subclass of BasePlugin".format(name, obj.__name__))
                continue

            # Make sure class is defined in this module or a submodule
            if inspect.getmodule(obj) is plugin_module or obj.__module__.startswith(name + '.'):
                already_added = obj in plugins

                log.info("Found plugin {} at {}.{} via pkgutil{}".format(obj.name, name, obj_name, " (already added)" if already_added else ""))

                if not already_added:
                    plugins.append(obj)

    print()
    print(plugins)
