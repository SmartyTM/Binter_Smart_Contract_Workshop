from decimal import Decimal
from unittest import TestCase

from ..types.attribute_data_types import AttributeDateTimeType, AttributeDecimalType
from ..types.attributes import Attribute

from .....utils.feature_flags import (
    ACCOUNT_ATTRIBUTE_HOOK,
    skip_if_not_enabled,
)

# <NOT RELEASE START: IMP_681_SERVICING_GROUPS>
from datetime import datetime
from zoneinfo import ZoneInfo

from ..types.attributes import AttributesObservation
from .....utils import exceptions
from .....utils.feature_flags import SERVICING_GROUPS

# <NOT RELEASE END>


class TestPublicCommonV400Attributes(TestCase):
    # Attribute

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_constructor_valid(self):
        Attribute(name="attribute", data_type=AttributeDecimalType())

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_constructor_raises_name_invalid(self):
        with self.assertRaises(exceptions.InvalidSmartContractError) as e:
            Attribute(name=" ", data_type=AttributeDateTimeType())
        expected = "'name' must be a non-empty string"

        self.assertEqual(expected, str(e.exception))

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_constructor_raises_name_none(self):
        with self.assertRaises(exceptions.StrongTypingError) as e:
            Attribute(name=None, data_type=AttributeDateTimeType())
        expected = "'name' expected str, got None"

        self.assertEqual(expected, str(e.exception))

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_constructor_raises_type_invalid(self):
        with self.assertRaises(exceptions.StrongTypingError) as e:
            Attribute(name="attribute", data_type=Decimal)
        expected = "'data_type' expected Union[AttributeDecimalType, AttributeDateTimeType, AttributeStringType], got '<class 'decimal.Decimal'>'"
        self.assertEqual(expected, str(e.exception))

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_constructor_type_valid_constructor_raises_not_called(self):
        with self.assertRaises(exceptions.StrongTypingError) as e:
            Attribute(name="attribute", data_type=AttributeDecimalType)
        expected = (
            "'data_type' expected Union[AttributeDecimalType, AttributeDateTimeType, AttributeStringType], got '<class 'vault.kernel.contracts."
            "contracts_language.public.versions.version_400.common.types.attribute_data_types.AttributeDecimalType'>'"
        )
        self.assertEqual(expected, str(e.exception))

    # <NOT RELEASE START: IMP_681_SERVICING_GROUPS>
    # AttributeObservation

    @skip_if_not_enabled(SERVICING_GROUPS)
    def test_attributes_observation_constructor_valid(self):
        AttributesObservation(
            attribute_values={
                "name-1": "value-1",
                "name-2": Decimal("2"),
                "name-3": datetime(2024, 3, 3, tzinfo=ZoneInfo("UTC")),
                "name-4": None,
            },
            value_datetime=datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")),
        )

    @skip_if_not_enabled(SERVICING_GROUPS)
    def test_attributes_observation_constructor_invalid_value_datetime(self):
        with self.assertRaises(exceptions.InvalidSmartContractError) as e:
            AttributesObservation(
                attribute_values={"name": "value"},
                value_datetime=datetime(2024, 1, 1),
            )
        expected = "'value_datetime' of AttributesObservation is not timezone aware."

        self.assertEqual(expected, str(e.exception))

    @skip_if_not_enabled(SERVICING_GROUPS)
    def test_attributes_observation_constructor_invalid_attribute_value_datetime(self):
        with self.assertRaises(exceptions.InvalidSmartContractError) as e:
            AttributesObservation(
                attribute_values={"name": datetime(2024, 1, 1)},
                value_datetime=datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC")),
            )
        expected = "'attribute_values[\"name\"]' of AttributesObservation is not timezone aware."

        self.assertEqual(expected, str(e.exception))

    @skip_if_not_enabled(SERVICING_GROUPS)
    def test_attributes_observation_dunder_methods_overridden(self):
        self.assertIsNot(AttributesObservation.__repr__, object.__repr__)
        self.assertIsNot(AttributesObservation.__eq__, object.__eq__)


# <NOT RELEASE END>
