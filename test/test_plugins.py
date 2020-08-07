# coding: utf-8
from __future__ import absolute_import

import pytest

import mcomix.plugins
from mcomix.plugins.base import TestingDummyPlugin
from mcomix.plugins.dummy_1 import DummyPlugin1
from mcomix.plugins.dummy_2 import DummyPlugin2


def test_dummy_plugin_count():
    dummies = [plugin for plugin in mcomix.plugins.get_plugins() if issubclass(plugin, TestingDummyPlugin)]

    assert len(dummies) == 2


@pytest.mark.parametrize("plugin,expected_name", [
    (DummyPlugin1, "DummyPlugin1"),
    (DummyPlugin2, "FooBarBaz"),
])
def test_get_plugin_names(plugin, expected_name):
    assert plugin.name == expected_name


entrypoints = dict([("{}:{}".format(ep.module_name, '.'.join(ep.attrs)), ep) for ep in mcomix.plugins._get_entrypoints()])


@pytest.mark.parametrize("plugin,exception", [
    (entrypoints['mcomix.plugins.dummy_1:DummyPlugin1'], None),
    (entrypoints['mcomix.plugins.dummy_1:NotAPlugin'], TypeError),
    (entrypoints['mcomix.plugins.dummy_1:DoesNotExist'], ImportError),
])
def test_entrypoint_loading(plugin, exception):
    if exception is not None:
        with pytest.raises(exception):
            mcomix.plugins._entrypoint_load_plugin(plugin, error=True)
    else:
        mcomix.plugins._entrypoint_load_plugin(plugin, error=True)


@pytest.mark.parametrize("name", mcomix.plugins.__all__)
def test_check_all(name):
    assert hasattr(mcomix.plugins, name), "__all__ contains non-existant name `{}`".format(name)
