import unittest

from named_entity_recognition.stanford import Stanford


class TestStanford(unittest.TestCase):
    def test_continue_elements(self):
        self.assertSequenceEqual(list(Stanford.get_continue_elements([])), []),
        self.assertSequenceEqual(list(Stanford.get_continue_elements([3])), [[3]]),
        self.assertSequenceEqual(
            list(Stanford.get_continue_elements([3, 6, 7])), [[3], [6, 7]]
        )
        self.assertSequenceEqual(
            list(Stanford.get_continue_elements([3, 6, 7, 9])), [[3], [6, 7], [9]]
        )


if __name__ == "__main__":
    unittest.main()
