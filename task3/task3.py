from typing import Protocol, runtime_checkable, Iterator

@runtime_checkable
class Plugin(Protocol):
    name: str

    def process(self, value: object) -> object:
        ...
class PluginError(ValueError):
    pass
class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: object) -> None:
        name = getattr(plugin, "name", None)
        process = getattr(plugin, "process", None)

        if not isinstance(plugin, Plugin):
            raise PluginError("plugin must have name and process")
        if not isinstance(name, str):
            raise PluginError("plugin name must be str")
        if not callable(process):
            raise PluginError("plugin process must be callable")
        if name in self._plugins:
            raise PluginError("duplicate plugin name")
        self._plugins[name] = plugin

    def unregister(self, name: str) -> None:
        if name not in self._plugins:
            raise PluginError("plugin not found")
        del self._plugins[name]

    def get(self, name: str) -> object:
        if name not in self._plugins:
            raise PluginError("plugin not found")
        return self._plugins[name]

    def __iter__(self) -> Iterator[object]:
        return iter(self._plugins.values())