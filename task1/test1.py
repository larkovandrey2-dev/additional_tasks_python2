import unittest

from task1 import StrictConfig


class TestStrictConfig(unittest.TestCase):
    def test_read_fields(self) -> None:
        cfg = StrictConfig(host="localhost", port=8080)

        self.assertEqual(cfg.host, "localhost")
        self.assertEqual(cfg.port, 8080)
        self.assertEqual(cfg.fields(), ("host", "port"))
        self.assertEqual(cfg.as_dict(), {"host": "localhost", "port": 8080})

    def test_cannot_add_new_field(self) -> None:
        cfg = StrictConfig(host="localhost")

        with self.assertRaises(AttributeError):
            cfg.potr = 123

    def test_field_can_have_name_as_method(self) -> None:
        cfg = StrictConfig(fields="my value")

        self.assertEqual(cfg.fields(), ("fields",))
        self.assertEqual(cfg.get("fields"), "my value")


if __name__ == "__main__":
    unittest.main()