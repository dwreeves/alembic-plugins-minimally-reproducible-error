import sys


def setup(plugin):
    print(f"actual-behavior-plugin: setup() called for plugin {plugin.name!r}")


modules = [sys.modules[__name__]]
