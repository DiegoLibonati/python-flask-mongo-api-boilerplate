from src.constants import codes, messages


class TestCodesAndMessages:
    def test_codes_are_strings(self) -> None:
        for name in dir(codes):
            if name.startswith("CODE_"):
                value = getattr(codes, name)
                assert isinstance(value, str), f"{name} debe ser string"

    def test_messages_are_strings(self) -> None:
        for name in dir(messages):
            if name.startswith("MESSAGE_"):
                value = getattr(messages, name)
                assert isinstance(value, str), f"{name} debe ser string"

    def test_codes_match_messages(self) -> None:
        code_names = [n for n in dir(codes) if n.startswith("CODE_")]

        for code_name in code_names:
            message_name = code_name.replace("CODE_", "MESSAGE_", 1)

            if hasattr(messages, message_name):
                message = getattr(messages, message_name)
                assert isinstance(message, str)
