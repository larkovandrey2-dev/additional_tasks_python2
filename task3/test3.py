import unittest

from task3 import PluginRegistry, PluginError

class UpperPlugin:
    name = "upper"

    def process(self, value: object) -> object:
        return str(value).upper()


class BadPlugin:
    name = "bad"
    process = 123


class TestPluginRegistry(unittest.TestCase):
    def test_register_and_get_plugin(self) -> None:
        registry = PluginRegistry()
        plugin = UpperPlugin()

        registry.register(plugin)

        self.assertIs(registry.get("upper"), plugin)
        self.assertEqual(plugin.process("hello"), "HELLO")

    def test_duplicate_name_is_error(self) -> None:
        registry = PluginRegistry()

        registry.register(UpperPlugin())

        with self.assertRaises(PluginError):
            registry.register(UpperPlugin())

    def test_bad_plugin(self) -> None:
        registry = PluginRegistry()

        with self.assertRaises(PluginError):
            registry.register(BadPlugin())

    def test_iteration_keeps_order(self) -> None:
        class LowerPlugin:
            name = "lower"

            def process(self, value: object) -> object:
                return str(value).lower()

        registry = PluginRegistry()
        registry.register(UpperPlugin())
        registry.register(LowerPlugin())

        self.assertEqual([plugin.name for plugin in registry], ["upper", "lower"])

        registry.unregister("upper")

        self.assertEqual([plugin.name for plugin in registry], ["lower"])


if __name__ == "__main__":
    unittest.main()
