"""Tests for MacStudio AI privacy routing."""

import importlib.util
from pathlib import Path
import unittest

ROUTING = (
    Path(__file__).parents[1]
    / "custom_components"
    / "macstudio_ai"
    / "routing.py"
)
spec = importlib.util.spec_from_file_location("macstudio_ai_routing", ROUTING)
assert spec and spec.loader
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)


class PrivacyRoutingTest(unittest.TestCase):
    def test_only_allowlisted_satellite_is_private(self) -> None:
        private = {"office"}
        self.assertTrue(
            routing.use_private_agent(
                device_id="office",
                user_id=None,
                private_devices=private,
                allow_private_text=True,
            )
        )
        self.assertFalse(
            routing.use_private_agent(
                device_id="living-room",
                user_id="admin",
                private_devices=private,
                allow_private_text=True,
            )
        )

    def test_authenticated_text_can_be_private(self) -> None:
        self.assertTrue(
            routing.use_private_agent(
                device_id=None,
                user_id="admin",
                private_devices=set(),
                allow_private_text=True,
            )
        )
        self.assertFalse(
            routing.use_private_agent(
                device_id=None,
                user_id=None,
                private_devices=set(),
                allow_private_text=True,
            )
        )

    def test_session_identity_isolated_by_source_and_conversation(self) -> None:
        first = routing.session_user(
            device_id="office", user_id=None, conversation_id="one"
        )
        second = routing.session_user(
            device_id="living-room", user_id=None, conversation_id="one"
        )
        follow_up = routing.session_user(
            device_id="office", user_id=None, conversation_id="one"
        )
        self.assertNotEqual(first, second)
        self.assertEqual(first, follow_up)


if __name__ == "__main__":
    unittest.main()
