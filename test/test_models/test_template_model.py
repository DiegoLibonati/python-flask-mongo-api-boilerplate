import pytest
from pydantic import ValidationError

from src.models.template_model import TemplateModel


class TestTemplateModel:
    def test_create_valid_template(self) -> None:
        template = TemplateModel(name="Valid Template")

        assert template.name == "Valid Template"

    def test_name_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TemplateModel(name="")

        errors = exc_info.value.errors()
        assert any("min_length" in str(e) or "at least 1" in str(e).lower() for e in errors)

    def test_name_strips_whitespace(self) -> None:
        template = TemplateModel(name="  Spaced Template  ")

        assert template.name == "Spaced Template"

    def test_name_only_whitespace_fails(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="   ")

    def test_name_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TemplateModel()

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_model_dump_returns_dict(self) -> None:
        template = TemplateModel(name="Test")
        result = template.model_dump()

        assert isinstance(result, dict)
        assert result == {"name": "Test"}

    def test_name_with_special_characters(self) -> None:
        special_names = [
            "Template-with-dashes",
            "Template_with_underscores",
            "Template.with.dots",
            "Template (with) parens",
            "Template 123",
            "Ñoño español",
            "日本語",
        ]

        for name in special_names:
            template = TemplateModel(name=name)
            assert template.name == name

    def test_name_with_single_character(self) -> None:
        template = TemplateModel(name="A")
        assert template.name == "A"

    def test_name_with_long_string(self) -> None:
        long_name = "A" * 1000
        template = TemplateModel(name=long_name)

        assert template.name == long_name
        assert len(template.name) == 1000

    def test_name_integer_fails_validation(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name=123)

    def test_name_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name=None)


class TestTemplateModelSerialization:
    def test_model_to_json(self) -> None:
        template = TemplateModel(name="JSON Test")
        json_str = template.model_dump_json()

        assert '"name":"JSON Test"' in json_str or '"name": "JSON Test"' in json_str

    def test_model_from_dict(self) -> None:
        data = {"name": "From Dict"}
        template = TemplateModel(**data)

        assert template.name == "From Dict"

    def test_model_validation_with_extra_fields(self) -> None:
        template = TemplateModel(name="Test", extra_field="ignored")

        assert template.name == "Test"
        assert not hasattr(template, "extra_field")
