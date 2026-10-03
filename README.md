# Alembic `alembic.plugins` entry point: docs vs. code

Alembic's [plugin docs](https://alembic.sqlalchemy.org/en/latest/api/plugins.html#making-a-plugin-installable)
say the `alembic.plugins` entry point value is "the module containing the `setup()` function":

```toml
[project.entry-points."alembic.plugins"]
mycompany.plugin_name = "mycompany.alembic_plugin"
```

But [`alembic/runtime/plugins.py`](https://github.com/sqlalchemy/alembic/blob/main/alembic/runtime/plugins.py)
iterates over whatever the entry point loads:

```python
def _setup() -> None:
    # setup third party plugins
    for entrypoint in metadata.entry_points(group="alembic.plugins"):
        for mod in entrypoint.load():
            Plugin.setup_plugin_from_module(mod, entrypoint.name)
```

So a plugin written the documented way breaks `import alembic` outright.
The only thing that works is pointing the entry point at an iterable of modules.

## Run it

Requires [uv](https://docs.astral.sh/uv/). Each script just does `import alembic`;
the only difference is which local plugin package its inline metadata installs.

```sh
uv run with_documented_behavior_plugin.py
uv run with_actual_behavior_plugin.py
```

## What you'll see

`with_documented_behavior_plugin.py` (entry point -> module, as documented):

```
Traceback (most recent call last):
  File ".../with_documented_behavior_plugin.py", line 8, in <module>
    import alembic
  ...
  File ".../alembic/runtime/plugins.py", line 203, in <module>
    _setup()
  File ".../alembic/runtime/plugins.py", line 199, in _setup
    for mod in entrypoint.load():
TypeError: 'module' object is not iterable
```

`with_actual_behavior_plugin.py` (entry point -> `modules = [sys.modules[__name__]]`):

```
actual-behavior-plugin: setup() called for plugin 'actual'
imported alembic 1.20.0
```

## Layout

```
documented-behavior-plugin/   pyproject.toml + one module; entry point = "documented_behavior_plugin"
actual-behavior-plugin/       pyproject.toml + one module; entry point = "actual_behavior_plugin:modules"
with_documented_behavior_plugin.py
with_actual_behavior_plugin.py
```

Observed with Alembic 1.20.0 (pinned in the scripts). The loader has been the same since
the plugin system landed in 1.18.0.
