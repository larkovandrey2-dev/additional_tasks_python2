import unittest

from task2 import ValidatedRecord,Field,ValidationError

class User(ValidatedRecord):
    name = Field(str)
    age = Field(int, min_value=0)


class Employee(User):
    salary = Field(int, min_value=0)


class TestValidatedRecord(unittest.TestCase):
    def test_create_and_change_record(self) -> None:
        user = User(name="Alice", age=20)

        user.age = 21

        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.age, 21)
        self.assertEqual(user.to_dict(), {"name": "Alice", "age": 21})

    def test_field_checks_type_and_min(self) -> None:
        user = User(name="Alice", age=20)

        with self.assertRaises(ValidationError):
            user.age = "old"

        with self.assertRaises(ValidationError):
            user.age = -1

    def test_two_objects(self) -> None:
        first = User(name="Alice", age=20)
        second = User(name="Bob", age=30)

        first.age = 21

        self.assertEqual(first.age, 21)
        self.assertEqual(second.age, 30)

    def test_schema(self) -> None:
        employee = Employee(name="Alice", age=20, salary=100)

        self.assertEqual(employee.to_dict(), {"name": "Alice", "age": 20, "salary": 100})
        self.assertEqual(Employee.schema()["salary"], {"type": "int", "min_value": 0})


if __name__ == "__main__":
    unittest.main()
