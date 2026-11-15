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
    def test_only_allowlisted_satellite_may_use_private_agent(self) -> None:
        private = {"office"}
        self.assertTrue(
            routing.private_context_allowed(
                device_id="office",
                user_id=None,
                private_devices=private,
                allow_private_text=True,
            )
        )
        self.assertFalse(
            routing.private_context_allowed(
                device_id="living-room",
                user_id="admin",
                private_devices=private,
                allow_private_text=True,
            )
        )

    def test_authenticated_text_can_be_private(self) -> None:
        self.assertTrue(
            routing.private_context_allowed(
                device_id=None,
                user_id="admin",
                private_devices=set(),
                allow_private_text=True,
            )
        )
        self.assertFalse(
            routing.private_context_allowed(
                device_id=None,
                user_id=None,
                private_devices=set(),
                allow_private_text=True,
            )
        )

    def test_document_requests_are_detected_without_matching_general_knowledge(self) -> None:
        self.assertTrue(routing.is_document_request("Suche die Gardena-Rechnung"))
        self.assertTrue(routing.is_document_request("Was steht in meinem Vertrag?"))
        self.assertFalse(routing.is_document_request("Wie groß ist der Pazifik?"))
        self.assertFalse(routing.is_document_request("Schalte das Licht im Flur ein"))
        self.assertTrue(
            routing.deny_document_request(
                text="Lies meine Rechnung vor", private_allowed=False
            )
        )
        self.assertFalse(
            routing.deny_document_request(
                text="Lies meine Rechnung vor", private_allowed=True
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

    def test_read_only_result_forbids_action_claim(self) -> None:
        guard = routing.action_claim_guard(
            tool_results=[("homeassistant__GetLiveContext", False)],
            read_only_tools={"homeassistant__GetLiveContext": True},
        )
        self.assertIn("keine Geräteaktion", guard)

    def test_successful_mutation_needs_no_action_guard(self) -> None:
        self.assertIsNone(
            routing.action_claim_guard(
                tool_results=[("HassTurnOn", False)],
                read_only_tools={"HassTurnOn": False},
            )
        )

    def test_failed_mutation_forbids_success_claim(self) -> None:
        guard = routing.action_claim_guard(
            tool_results=[("HassTurnOn", True)],
            read_only_tools={"HassTurnOn": False},
        )
        self.assertIn("keine Geräteaktion erfolgreich", guard)


if __name__ == "__main__":
    unittest.main()
