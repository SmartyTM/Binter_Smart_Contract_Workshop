import unittest
from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock, call, patch


from ..types import (
    BalancesFilter,
    BalancesIntervalFetcher,
    BalancesObservationFetcher,
    DefinedDateTime,
    fetchers,
    
    FlagsFilter,
    FlagsIntervalFetcher,
    FlagsObservationFetcher,
    IntervalFetcher,
    ParametersFilter,
    ParametersIntervalFetcher,
    ParametersObservationFetcher,
    PostingsIntervalFetcher,
    RelativeDateTime,
    Shift,
    
)
from .....utils.types_utils import (
    ContractsLanguageDunderMixin,
)
from .....utils.exceptions import (
    StrongTypingError,
    InvalidSmartContractError,
)

from .....utils.feature_flags import (
    
    disable_fflags,
    is_fflag_enabled,
    
    skip_if_not_enabled,
)


class TestPublicCommonV400IntervalFetcher(TestCase):
    @patch.object(IntervalFetcher, "_validate_attributes")
    def test_interval_constructor_calls_validation(self, mock_validate_attributes: Mock):
        IntervalFetcher(fetcher_id="fetcher_id", start=DefinedDateTime.EFFECTIVE_DATETIME)
        mock_validate_attributes.assert_called_once()

    @patch.object(fetchers.types_utils, "validate_type")
    def test_interval_validate_attributes_called_for_all_attributes(self, mock_validate_type: Mock):
        interval_fetcher = IntervalFetcher(
            fetcher_id="fetcher_id", start=DefinedDateTime.EFFECTIVE_DATETIME
        )
        mock_validate_type.assert_has_calls(
            [
                call(
                    interval_fetcher.fetcher_id,
                    str,
                    hint="str",
                    check_empty=True,
                    prefix="IntervalFetcher.fetcher_id",
                ),
                call(
                    interval_fetcher.start,
                    (DefinedDateTime, RelativeDateTime),
                    hint="Union[RelativeDateTime, DefinedDateTime]",
                    prefix="IntervalFetcher.start",
                ),
                call(
                    interval_fetcher.end,
                    (DefinedDateTime, RelativeDateTime),
                    hint="Union[RelativeDateTime, DefinedDateTime]",
                    is_optional=True,
                    prefix="IntervalFetcher.end",
                ),
            ]
        )


class TestPublicCommonV400BalancesIntervalFetcher(TestCase):
    def test_balances_interval_fetcher_repr(self):
        self.assertTrue(
            issubclass(BalancesIntervalFetcher, ContractsLanguageDunderMixin),
        )
        self.assertIn(
            "BalancesIntervalFetcher",
            repr(BalancesIntervalFetcher),
        )

    def test_balances_interval_fetcher_equality(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual(balances_interval_fetcher, other_balances_interval_fetcher)

    def test_balances_interval_fetcher_unequal_start(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=4)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertNotEqual(balances_interval_fetcher, other_balances_interval_fetcher)

    def test_balances_interval_fetcher_with_relative_datetime_start(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual("fetcher_id", balances_interval_fetcher.fetcher_id)

        self.assertEqual(-1, balances_interval_fetcher.start.shift.years)
        self.assertEqual(2, balances_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, balances_interval_fetcher.end)

    def test_balances_interval_fetcher_errors_without_start(self):
        with self.assertRaises(TypeError) as e:
            BalancesIntervalFetcher(fetcher_id="fetcher_id", end=DefinedDateTime.EFFECTIVE_DATETIME)
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'start'",
        )

    def test_balances_interval_fetcher_errors_without_id(self):
        with self.assertRaises(TypeError) as e:
            BalancesIntervalFetcher(
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'fetcher_id'",
        )

    def test_balances_interval_fetcher_errors_with_empty_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesIntervalFetcher(
                fetcher_id="",
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "'BalancesIntervalFetcher.fetcher_id' must be a non-empty string",
        )

    def test_balances_interval_fetcher_succeeds_without_end(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
        )
        self.assertEqual("fetcher_id", balances_interval_fetcher.fetcher_id)

        self.assertEqual(-1, balances_interval_fetcher.start.shift.years)
        self.assertEqual(2, balances_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.LIVE, balances_interval_fetcher.end)

    def test_balances_interval_fetcher_with_defined_datetime_start(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id", start=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual("fetcher_id", balances_interval_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, balances_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, balances_interval_fetcher.end)

    def test_balances_interval_fetcher_errors_with_live_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.LIVE,
            )
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher 'start' cannot be set to 'DefinedDateTime.LIVE'",
        )

    def test_balances_interval_fetcher_between_effective_and_live(self):
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
        )
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, balances_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, balances_interval_fetcher.end)

    def test_balances_interval_fetcher_errors_with_invalid_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher 'start' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_balances_interval_fetcher_errors_with_invalid_end(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher 'end' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_balances_interval_fetcher_errors_with_invalid_start_origin(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=RelativeDateTime(
                    origin=DefinedDateTime.INTERVAL_START, shift=Shift(years=-1)
                ),
            )
        self.assertEqual(
            str(e.exception),
            "BalancesIntervalFetcher 'start' origin value must be set to "
            "'DefinedDateTime.EFFECTIVE_DATETIME'",
        )

    def test_balances_interval_fetcher_with_filter(self):
        filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        balances_interval_fetcher = BalancesIntervalFetcher(
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=filter,
        )
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, balances_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, balances_interval_fetcher.end)
        self.assertEqual(filter, balances_interval_fetcher.filter)

    def test_balances_interval_fetcher_raises_with_invalid_filter_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.LIVE,
                filter=123,
            )

        self.assertEqual(
            str(e.exception),
            "'BalancesIntervalFetcher.filter' expected BalancesFilter if populated, got '123' of "
            "type int",
        )

    def test_balances_interval_fetcher_raises_with_invalid_start_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'BalancesIntervalFetcher.start' expected Union[RelativeDateTime, DefinedDateTime], "
            "got 'foo' of type str",
        )

    def test_balances_interval_fetcher_raises_with_invalid_end_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'BalancesIntervalFetcher.end' expected Union[RelativeDateTime, DefinedDateTime] if "
            "populated, got 'foo' of type str",
        )





class TestPublicCommonV400BalancesObservationFetcher(TestCase):
    def test_balances_observation_fetcher_repr(self):
        self.assertTrue(
            issubclass(BalancesObservationFetcher, ContractsLanguageDunderMixin),
        )
        self.assertIn(
            "BalancesObservationFetcher",
            repr(BalancesObservationFetcher),
        )

    def test_balances_observation_fetcher_equality(self):
        filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        other_filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        other_balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=other_filter
        )

        self.assertEqual(balances_observation_fetcher, other_balances_observation_fetcher)

    def test_balances_observation_fetcher_unequal_filter(self):
        filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        other_filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS42"])
        other_balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=other_filter
        )

        self.assertNotEqual(balances_observation_fetcher, other_balances_observation_fetcher)

    def test_balances_observation_fetcher_with_defined_datetime(self):
        filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        self.assertEqual("fetcher_id", balances_observation_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, balances_observation_fetcher.at)
        self.assertEqual(filter, balances_observation_fetcher.filter)

    def test_balances_observation_fetcher_with_relative_datetime(self):
        filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id", at=relative_date_time, filter=filter
        )
        self.assertEqual("fetcher_id", balances_observation_fetcher.fetcher_id)
        self.assertEqual(relative_date_time, balances_observation_fetcher.at)
        self.assertEqual(filter, balances_observation_fetcher.filter)

    def test_balances_observation_fetcher_with_no_filter(self):
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        balances_observation_fetcher = BalancesObservationFetcher(
            fetcher_id="fetcher_id",
            at=relative_date_time,
        )
        self.assertEqual("fetcher_id", balances_observation_fetcher.fetcher_id)
        self.assertEqual(relative_date_time, balances_observation_fetcher.at)

    def test_balances_observation_fetcher_raises_with_empty_fetcher_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservationFetcher(
                fetcher_id="",
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                ),
            )

        self.assertEqual(
            str(e.exception), "'BalancesObservationFetcher.fetcher_id' must be a non-empty string"
        )

    def test_balances_observation_fetcher_raises_with_fetcher_id_not_populated(self):
        with self.assertRaises(TypeError) as e:
            BalancesObservationFetcher(
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                )
            )

        self.assertEqual(
            str(e.exception),
            "BalancesObservationFetcher.__init__() missing 1 "
            "required positional argument: 'fetcher_id'",
        )

    def test_balances_observation_fetcher_raises_with_fetcher_id_invalid_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesObservationFetcher(
                fetcher_id=42,
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                ),
            )

        self.assertEqual(
            str(e.exception),
            "'BalancesObservationFetcher.fetcher_id' expected str, got '42' of type int",
        )

    def test_balances_observation_fetcher_raises_if_at_attribute_not_populated(self):
        with self.assertRaises(TypeError) as e:
            BalancesObservationFetcher(
                fetcher_id="fetcher_id",
            )

        self.assertEqual(
            str(e.exception),
            "BalancesObservationFetcher.__init__() missing 1 " "required positional argument: 'at'",
        )

    def test_balances_observation_fetcher_raises_if_at_populated_with_interval_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservationFetcher(
                fetcher_id="fetcher_id",
                at=DefinedDateTime.INTERVAL_START,
            )

        self.assertEqual(
            str(e.exception),
            "BalancesObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_balances_observation_fetcher_raises_if_at_origin_populated_with_interval_start(self):
        relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.INTERVAL_START, shift=Shift(months=-1)
        )
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservationFetcher(
                fetcher_id="fetcher_id",
                at=relative_date_time,
            )

        self.assertEqual(
            str(e.exception),
            "BalancesObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_balances_observation_fetcher_raises_with_invalid_filter_type(self):
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        with self.assertRaises(StrongTypingError) as e:
            BalancesObservationFetcher(fetcher_id="fetcher_id", at=relative_date_time, filter=123)
        self.assertEqual(
            str(e.exception),
            "'BalancesObservationFetcher.filter' expected BalancesFilter if populated, got '123' "
            "of type int",
        )

    def test_balances_observation_fetcher_raises_with_invalid_at_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesObservationFetcher(fetcher_id="fetcher_id", at="foo")
        self.assertEqual(
            str(e.exception),
            "'BalancesObservationFetcher.at' expected Union[DefinedDateTime, RelativeDateTime], "
            "got 'foo' of type str",
        )


class TestPublicCommonV400PostingsIntervalFetcher(TestCase):
    def test_postings_interval_fetcher_repr(self):
        self.assertTrue(
            issubclass(PostingsIntervalFetcher, ContractsLanguageDunderMixin),
        )
        self.assertIn(
            "PostingsIntervalFetcher",
            repr(PostingsIntervalFetcher),
        )

    def test_postings_interval_fetcher_equality(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual(postings_interval_fetcher, other_postings_interval_fetcher)

    def test_postings_interval_fetcher_unequal_start(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=4)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertNotEqual(postings_interval_fetcher, other_postings_interval_fetcher)

    def test_postings_interval_fetcher_with_relative_datetime_start(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual("fetcher_id", postings_interval_fetcher.fetcher_id)

        self.assertEqual(-1, postings_interval_fetcher.start.shift.years)
        self.assertEqual(2, postings_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, postings_interval_fetcher.end)

    def test_postings_interval_fetcher_errors_without_start(self):
        with self.assertRaises(TypeError) as e:
            PostingsIntervalFetcher(fetcher_id="fetcher_id", end=DefinedDateTime.EFFECTIVE_DATETIME)
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'start'",
        )

    def test_postings_interval_fetcher_errors_without_id(self):
        with self.assertRaises(TypeError) as e:
            PostingsIntervalFetcher(
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'fetcher_id'",
        )

    def test_postings_interval_fetcher_errors_with_empty_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            PostingsIntervalFetcher(
                fetcher_id="",
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "'PostingsIntervalFetcher.fetcher_id' must be a non-empty string",
        )

    def test_postings_interval_fetcher_succeeds_without_end(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
        )
        self.assertEqual("fetcher_id", postings_interval_fetcher.fetcher_id)

        self.assertEqual(-1, postings_interval_fetcher.start.shift.years)
        self.assertEqual(2, postings_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.LIVE, postings_interval_fetcher.end)

    def test_postings_interval_fetcher_with_defined_datetime_start(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id", start=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual("fetcher_id", postings_interval_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, postings_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, postings_interval_fetcher.end)

    def test_postings_interval_fetcher_errors_with_live_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.LIVE,
            )
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher 'start' cannot be set to 'DefinedDateTime.LIVE'",
        )

    def test_postings_interval_fetcher_between_effective_and_live(self):
        postings_interval_fetcher = PostingsIntervalFetcher(
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
        )
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, postings_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, postings_interval_fetcher.end)

    def test_postings_interval_fetcher_errors_with_invalid_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher 'start' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_postings_interval_fetcher_errors_with_invalid_end(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher 'end' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_postings_interval_fetcher_errors_with_invalid_start_origin(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start=RelativeDateTime(
                    origin=DefinedDateTime.INTERVAL_START, shift=Shift(years=-1)
                ),
            )
        self.assertEqual(
            str(e.exception),
            "PostingsIntervalFetcher 'start' origin value must be set to "
            "'DefinedDateTime.EFFECTIVE_DATETIME'",
        )

        

    def test_postings_interval_fetcher_raises_with_invalid_start_type(self):
        with self.assertRaises(StrongTypingError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'PostingsIntervalFetcher.start' expected Union[RelativeDateTime, DefinedDateTime], "
            "got 'foo' of type str",
        )

    def test_postings_interval_fetcher_raises_with_invalid_end_type(self):
        with self.assertRaises(StrongTypingError) as e:
            PostingsIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'PostingsIntervalFetcher.end' expected Union[RelativeDateTime, DefinedDateTime] if "
            "populated, got 'foo' of type str",
        )


class TestPublicCommonV400ParametersIntervalFetcher(TestCase):
    def test_parameters_interval_fetcher_repr(self):
        fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        expected = (
            "ParametersIntervalFetcher(fetcher_id='fetcher_id', "
            + "start=RelativeDateTime(origin=DefinedDateTime.EFFECTIVE_DATETIME, "
            + "shift=Shift(years=-1, months=2, days=None, "
            + "hours=None, minutes=None, seconds=None), find=None), "
            + "end=DefinedDateTime.EFFECTIVE_DATETIME, filter=None)"
        )
        self.assertEqual(expected, repr(fetcher))

    def test_parameters_interval_fetcher_equality(self):
        parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual(parameters_interval_fetcher, other_parameters_interval_fetcher)

    def test_parameters_interval_fetcher_unequal_start(self):
        parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )
        other_parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=4)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertNotEqual(parameters_interval_fetcher, other_parameters_interval_fetcher)

    def test_parameters_interval_fetcher_with_relative_datetime_start(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1"])
        parameters_interval_fetcher = ParametersIntervalFetcher(
            filter=filter,
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
        )

        self.assertEqual(filter, parameters_interval_fetcher.filter)
        self.assertEqual("fetcher_id", parameters_interval_fetcher.fetcher_id)
        self.assertEqual(-1, parameters_interval_fetcher.start.shift.years)
        self.assertEqual(2, parameters_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.end)

    def test_parameters_interval_fetcher_errors_without_start(self):
        with self.assertRaises(TypeError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'start'",
        )

    def test_parameters_interval_fetcher_errors_without_id(self):
        with self.assertRaises(TypeError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'fetcher_id'",
        )

    def test_parameters_interval_fetcher_errors_with_empty_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="",
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception), "'ParametersIntervalFetcher.fetcher_id' must be a non-empty string"
        )

    def test_parameters_interval_fetcher_errors_with_leading_underscore_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="_fetcher_id",
                start=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
                ),
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher 'fetcher_id' cannot start with an underscore",
        )

    def test_parameters_interval_fetcher_succeeds_without_end(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1"])
        parameters_interval_fetcher = ParametersIntervalFetcher(
            filter=filter,
            fetcher_id="fetcher_id",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
        )
        self.assertEqual(filter, parameters_interval_fetcher.filter)
        self.assertEqual("fetcher_id", parameters_interval_fetcher.fetcher_id)
        self.assertEqual(-1, parameters_interval_fetcher.start.shift.years)
        self.assertEqual(2, parameters_interval_fetcher.start.shift.months)
        self.assertEqual(DefinedDateTime.LIVE, parameters_interval_fetcher.end)

    def test_parameters_interval_fetcher_errors_with_live_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                start=DefinedDateTime.LIVE,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher 'start' cannot be set to 'DefinedDateTime.LIVE'",
        )

    def test_parameters_interval_fetcher_with_live_end(self):
        fetcher_filter = ParametersFilter(parameter_ids=["PARAMETER_1"])
        parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=fetcher_filter,
        )
        self.assertEqual("fetcher_id", parameters_interval_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.LIVE, parameters_interval_fetcher.end)
        self.assertEqual(fetcher_filter, parameters_interval_fetcher.filter)

    def test_parameters_interval_fetcher_errors_with_invalid_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                start=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher 'start' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_parameters_interval_fetcher_errors_with_invalid_end(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher 'end' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_parameters_interval_fetcher_errors_with_invalid_start_origin(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                start=RelativeDateTime(
                    origin=DefinedDateTime.INTERVAL_START, shift=Shift(years=-1)
                ),
            )
        self.assertEqual(
            str(e.exception),
            "ParametersIntervalFetcher 'start' origin value must be set to "
            "'DefinedDateTime.EFFECTIVE_DATETIME'",
        )

    def test_parameters_interval_fetcher_with_filter(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        parameters_interval_fetcher = ParametersIntervalFetcher(
            filter=filter,
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=RelativeDateTime(origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=1)),
        )
        self.assertEqual(filter, parameters_interval_fetcher.filter)
        self.assertEqual("fetcher_id", parameters_interval_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.end.origin)
        self.assertEqual(1, parameters_interval_fetcher.end.shift.years)

    def test_parameters_interval_fetcher_errors_with_empty_filter(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=[]),
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=1)
                ),
            )
        self.assertEqual(
            str(e.exception),
            "'ParametersFilter.parameter_ids' must be a non empty list, got []",
        )

    def test_parameters_interval_fetcher_without_filter_defaults_to_all_expected_parameters(self):
        parameters_interval_fetcher = ParametersIntervalFetcher(
            fetcher_id="fetcher_id",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=RelativeDateTime(origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=1)),
        )
        self.assertEqual("fetcher_id", parameters_interval_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.start)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_interval_fetcher.end.origin)
        self.assertEqual(1, parameters_interval_fetcher.end.shift.years)

    def test_parameters_interval_fetcher_errors_with_equal_start_and_end(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersIntervalFetcher(
                filter=ParametersFilter(parameter_ids=["PARAMETER_1"]),
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.EFFECTIVE_DATETIME,
            )
        self.assertEqual(
            str(e.exception), "ParametersIntervalFetcher 'start' cannot be equal to 'end'"
        )

    def test_parameters_interval_fetcher_raises_with_invalid_filter_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=RelativeDateTime(
                    origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=1)
                ),
                filter=123,
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersIntervalFetcher.filter' expected ParametersFilter if populated, got '123' "
            "of type int",
        )

    def test_parameters_interval_fetcher_raises_with_invalid_start_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersIntervalFetcher(
                fetcher_id="fetcher_id",
                start="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersIntervalFetcher.start' expected Union[RelativeDateTime, DefinedDateTime], "
            "got 'foo' of type str",
        )

    def test_parameters_interval_fetcher_raises_with_invalid_end_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersIntervalFetcher(
                fetcher_id="fetcher_id",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end="foo",
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersIntervalFetcher.end' expected Union[RelativeDateTime, DefinedDateTime] if "
            "populated, got 'foo' of type str",
        )


class TestPublicCommonV400ParametersObservationFetcher(TestCase):
    def test_parameters_observation_fetcher_repr(self):
        fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id",
            at=DefinedDateTime.EFFECTIVE_DATETIME,
            filter=ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"]),
        )
        expected = (
            "ParametersObservationFetcher(fetcher_id='fetcher_id', "
            + "at=DefinedDateTime.EFFECTIVE_DATETIME, "
            + "filter=ParametersFilter(parameter_ids=['PARAMETER_1', 'PARAMETER_2']))"
        )
        self.assertEqual(expected, repr(fetcher))

    def test_parameters_observation_fetcher_equality(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        other_filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        other_parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=other_filter
        )

        self.assertEqual(parameters_observation_fetcher, other_parameters_observation_fetcher)

    def test_parameters_observation_fetcher_unequal_filter(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        other_filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_42"])
        other_parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=other_filter
        )

        self.assertNotEqual(parameters_observation_fetcher, other_parameters_observation_fetcher)

    def test_parameters_observation_fetcher_with_defined_datetime(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=filter
        )
        self.assertEqual("fetcher_id", parameters_observation_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, parameters_observation_fetcher.at)
        self.assertEqual(filter, parameters_observation_fetcher.filter)

    def test_parameters_observation_fetcher_with_relative_datetime(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id", at=relative_date_time, filter=filter
        )
        self.assertEqual("fetcher_id", parameters_observation_fetcher.fetcher_id)
        self.assertEqual(relative_date_time, parameters_observation_fetcher.at)
        self.assertEqual(filter, parameters_observation_fetcher.filter)

    def test_parameters_observation_fetcher_with_no_filter(self):
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id",
            at=relative_date_time,
        )
        self.assertEqual("fetcher_id", parameters_observation_fetcher.fetcher_id)
        self.assertEqual(relative_date_time, parameters_observation_fetcher.at)

    def test_parameters_observation_fetcher_raises_with_empty_fetcher_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservationFetcher(
                fetcher_id="",
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                ),
            )

        self.assertEqual(
            str(e.exception), "'ParametersObservationFetcher.fetcher_id' must be a non-empty string"
        )

    def test_parameters_observation_fetcher_raises_with_leading_underscore_fetcher_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservationFetcher(
                fetcher_id="_fetcher_id",
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                ),
            )

        self.assertEqual(
            str(e.exception),
            "ParametersObservationFetcher 'fetcher_id' cannot start with an underscore",
        )

    def test_parameters_observation_fetcher_raises_with_fetcher_id_not_populated(self):
        with self.assertRaises(TypeError) as e:
            ParametersObservationFetcher(
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                )
            )

        self.assertEqual(
            str(e.exception),
            "ParametersObservationFetcher.__init__() missing 1 "
            "required positional argument: 'fetcher_id'",
        )

    def test_parameters_observation_fetcher_raises_with_fetcher_id_incorrect_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersObservationFetcher(
                fetcher_id=42,
                at=RelativeDateTime(
                    shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
                ),
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersObservationFetcher.fetcher_id' expected str, got '42' of type int",
        )

    def test_parameters_observation_fetcher_raises_if_at_attribute_not_populated(self):
        with self.assertRaises(TypeError) as e:
            ParametersObservationFetcher(
                fetcher_id="fetcher_id",
            )

        self.assertEqual(
            str(e.exception),
            "ParametersObservationFetcher.__init__() missing 1 required positional argument: 'at'",
        )

    def test_parameters_observation_fetcher_raises_if_at_populated_with_interval_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservationFetcher(
                fetcher_id="fetcher_id",
                at=DefinedDateTime.INTERVAL_START,
            )

        self.assertEqual(
            str(e.exception),
            "ParametersObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_parameters_observation_fetcher_raises_if_at_origin_populated_with_interval_start(self):
        relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.INTERVAL_START, shift=Shift(months=-1)
        )
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservationFetcher(
                fetcher_id="fetcher_id",
                at=relative_date_time,
            )

        self.assertEqual(
            str(e.exception),
            "ParametersObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_parameters_observation_fetcher_with_at_populated_with_live(self):
        parameters_observation_fetcher = ParametersObservationFetcher(
            fetcher_id="fetcher_id",
            at=DefinedDateTime.LIVE,
        )

        self.assertEqual("fetcher_id", parameters_observation_fetcher.fetcher_id)
        self.assertEqual(DefinedDateTime.LIVE, parameters_observation_fetcher.at)

    def test_parameters_observation_fetcher_raises_if_at_invalid_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersObservationFetcher(
                fetcher_id="fetcher_id",
                at=[2, 3],
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersObservationFetcher.at' expected Union[DefinedDateTime, RelativeDateTime], "
            "got '[2, 3]' of type list",
        )

    def test_parameters_observation_fetcher_raises_with_invalid_filter_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersObservationFetcher(
                fetcher_id="fetcher_id", at=DefinedDateTime.EFFECTIVE_DATETIME, filter=123
            )

        self.assertEqual(
            str(e.exception),
            "'ParametersObservationFetcher.filter' expected ParametersFilter if populated, got "
            "'123' of type int",
        )

    def test_parameters_observation_fetcher_raises_with_invalid_at_type(self):
        with self.assertRaises(StrongTypingError) as e:
            ParametersObservationFetcher(fetcher_id="fetcher_id", at="foo")

        self.assertEqual(
            str(e.exception),
            "'ParametersObservationFetcher.at' expected Union[DefinedDateTime, RelativeDateTime], "
            "got 'foo' of type str",
        )


class TestPublicCommonV400FlagsIntervalFetcher(TestCase):
    def test_flags_interval_fetcher_with_filter(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        self.assertEqual("flags_if_1", flags_if_1.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, flags_if_1.start)
        self.assertEqual(DefinedDateTime.LIVE, flags_if_1.end)
        self.assertEqual(FlagsFilter(flag_definition_ids=["flag_def_1"]), flags_if_1.filter)

    def test_flags_interval_fetcher_filter_not_populated(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
        )
        self.assertEqual("flags_if_1", flags_if_1.fetcher_id)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, flags_if_1.start)
        self.assertEqual(DefinedDateTime.LIVE, flags_if_1.end)
        self.assertIsNone(flags_if_1.filter)

    def test_flags_interval_fetcher_relative_datetime(self):
        start_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        end_time = RelativeDateTime(
            shift=Shift(months=1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        flags_if_1 = FlagsIntervalFetcher(fetcher_id="flags_if_1", start=start_time, end=end_time)
        self.assertEqual(start_time, flags_if_1.start)
        self.assertEqual(end_time, flags_if_1.end)
        self.assertEqual("flags_if_1", flags_if_1.fetcher_id)
        self.assertIsNone(flags_if_1.filter)

    def test_flags_interval_fetcher_check_default_end_is_live(self):
        flags_if = FlagsIntervalFetcher(
            fetcher_id="flags_if_1s", start=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual(DefinedDateTime.LIVE, flags_if.end)

    def test_flags_interval_fetcher_fetcher_id_not_populated_raises_error(self):
        with self.assertRaises(TypeError) as e:
            FlagsIntervalFetcher(start=DefinedDateTime.EFFECTIVE_DATETIME, end=DefinedDateTime.LIVE)
        self.assertEqual(
            "FlagsIntervalFetcher.__init__() missing 1 "
            "required keyword-only argument: 'fetcher_id'",
            str(e.exception),
        )

    def test_flags_interval_fetcher_fetcher_id_empty_string_raises_error(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsIntervalFetcher(
                fetcher_id="", start=DefinedDateTime.EFFECTIVE_DATETIME, end=DefinedDateTime.LIVE
            )
        self.assertEqual(
            "'FlagsIntervalFetcher.fetcher_id' must be a non-empty string",
            str(e.exception),
        )

    def test_flags_interval_fetcher_start_attribute_not_populated_raises_error(self):
        with self.assertRaises(TypeError) as e:
            FlagsIntervalFetcher(fetcher_id="flags_if_1", end=DefinedDateTime.LIVE)
        self.assertEqual(
            "FlagsIntervalFetcher.__init__() missing 1 " "required keyword-only argument: 'start'",
            str(e.exception),
        )

    def test_flags_interval_fetcher_fetcher_id_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsIntervalFetcher(
                fetcher_id=1, start=DefinedDateTime.EFFECTIVE_DATETIME, end=DefinedDateTime.LIVE
            )
        self.assertEqual(
            "'FlagsIntervalFetcher.fetcher_id' expected str, got '1' of type int",
            str(e.exception),
        )

    def test_flags_interval_fetcher_start_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsIntervalFetcher(fetcher_id="flags_if_1", start=1, end=DefinedDateTime.LIVE)
        self.assertEqual(
            (
                "'FlagsIntervalFetcher.start' expected Union[RelativeDateTime, DefinedDateTime], "
                "got '1' of type int"
            ),
            str(e.exception),
        )

    def test_flags_interval_fetcher_end_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsIntervalFetcher(
                fetcher_id="flags_if_1", start=DefinedDateTime.EFFECTIVE_DATETIME, end=1
            )
        self.assertEqual(
            (
                "'FlagsIntervalFetcher.end' expected Union[RelativeDateTime, DefinedDateTime] if "
                "populated, got '1' of type int"
            ),
            str(e.exception),
        )

    def test_flags_interval_fetcher_end_none_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsIntervalFetcher(
                fetcher_id="flags_if", start=DefinedDateTime.EFFECTIVE_DATETIME, end=None
            )
        self.assertEqual(
            "'FlagsIntervalFetcher.end' expected Union[RelativeDateTime, DefinedDateTime], got None",
            str(e.exception),
        )

    def test_flags_interval_fetcher_filter_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsIntervalFetcher(
                fetcher_id="flags_if_1",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.LIVE,
                filter=1,
            )
        self.assertEqual(
            "'FlagsIntervalFetcher.filter' expected FlagsFilter if populated, got '1' of type int",
            str(e.exception),
        )

    def test_flags_interval_fetcher_equality(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
        )
        flags_if_2 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
        )
        self.assertEqual(flags_if_1, flags_if_2)

    def test_flags_interval_fetcher_equality_with_filter(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        flags_if_2 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        self.assertEqual(flags_if_1, flags_if_2)

    def test_flags_interval_fetcher_unequal_different_fetcher_id(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        flags_if_2 = FlagsIntervalFetcher(
            fetcher_id="flags_if_222",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        self.assertNotEqual(flags_if_1, flags_if_2)

    def test_flags_interval_fetcher_unequal_different_end(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        flags_if_2 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=RelativeDateTime(
                origin=DefinedDateTime.EFFECTIVE_DATETIME, shift=Shift(years=-1, months=2)
            ),
            end=DefinedDateTime.EFFECTIVE_DATETIME,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        self.assertNotEqual(flags_if_1, flags_if_2)

    def test_flags_interval_fetcher_unequal_different_filter(self):
        flags_if_1 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
        )
        flags_if_2 = FlagsIntervalFetcher(
            fetcher_id="flags_if_1",
            start=DefinedDateTime.EFFECTIVE_DATETIME,
            end=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["flag_def_2"]),
        )
        self.assertNotEqual(flags_if_1, flags_if_2)

    def test_flags_interval_fetcher_start_equal_end_raises_error(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsIntervalFetcher(
                fetcher_id="flags_if_1",
                start=DefinedDateTime.EFFECTIVE_DATETIME,
                end=DefinedDateTime.EFFECTIVE_DATETIME,
                filter=FlagsFilter(flag_definition_ids=["flag_def_1"]),
            )
        self.assertEqual("FlagsIntervalFetcher 'start' cannot be equal to 'end'", str(e.exception))


class TestPublicCommonV400FlagsObservationFetcher(TestCase):
    def test_flags_observation_fetcher_filter_not_populated(self):
        flags_of = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual("flags_of_1", flags_of.fetcher_id)
        self.assertIs(DefinedDateTime.EFFECTIVE_DATETIME, flags_of.at)
        self.assertIsNone(flags_of.filter)

    def test_flags_observation_fetcher_with_filter(self):
        flags_of = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.EFFECTIVE_DATETIME,
            filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
        )
        self.assertEqual("flags_of_1", flags_of.fetcher_id)
        self.assertIs(DefinedDateTime.EFFECTIVE_DATETIME, flags_of.at)
        self.assertEqual(FlagsFilter(flag_definition_ids=["id1", "id2"]), flags_of.filter)

    def test_flags_observation_fetcher_with_relative_datetime(self):
        relative_date_time = RelativeDateTime(
            shift=Shift(months=-1), origin=DefinedDateTime.EFFECTIVE_DATETIME
        )
        flags_of = FlagsObservationFetcher(fetcher_id="flags_of_1", at=relative_date_time)
        self.assertEqual(relative_date_time, flags_of.at)
        self.assertEqual("flags_of_1", flags_of.fetcher_id)

    def test_flags_observation_fetcher_with_defined_datetime(self):
        flags_of = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME, flags_of.at)
        self.assertEqual("flags_of_1", flags_of.fetcher_id)

    def test_flags_observation_fetcher_fetcher_id_not_populated_raises_error(self):
        with self.assertRaises(TypeError) as e:
            FlagsObservationFetcher(
                at=DefinedDateTime.EFFECTIVE_DATETIME,
                filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
            )
        self.assertEqual(
            "FlagsObservationFetcher.__init__() missing 1 "
            "required positional argument: 'fetcher_id'",
            str(e.exception),
        )

    def test_flags_observation_fetcher_fetcher_id_empty_string_raises_error(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsObservationFetcher(fetcher_id="", at=DefinedDateTime.EFFECTIVE_DATETIME)
        self.assertEqual(
            "'FlagsObservationFetcher.fetcher_id' must be a non-empty string",
            str(e.exception),
        )

    def test_flags_observation_fetcher_at_attribute_not_populated_raises_error(self):
        with self.assertRaises(TypeError) as e:
            FlagsObservationFetcher(
                fetcher_id="flags_of_1", filter=FlagsFilter(flag_definition_ids=["id1", "id2"])
            )
        self.assertEqual(
            "FlagsObservationFetcher.__init__() missing 1 " "required positional argument: 'at'",
            str(e.exception),
        )

    def test_flags_observation_fetcher_equality(self):
        flags_of_1 = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.EFFECTIVE_DATETIME,
            filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
        )
        flags_of_2 = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.EFFECTIVE_DATETIME,
            filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
        )
        self.assertEqual(flags_of_1, flags_of_2)

    def test_flags_observation_fetcher_equality_no_filter(self):
        flags_of_1 = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        flags_of_2 = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertEqual(flags_of_1, flags_of_2)

    def test_flags_observation_fetcher_unequal_by_fetcher_id(self):
        flags_of_1 = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        flags_of_2 = FlagsObservationFetcher(
            fetcher_id="flags_of_2", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        self.assertNotEqual(flags_of_1, flags_of_2)

    def test_flags_observation_fetcher_unequal_by_at_attribute(self):
        flags_of_1 = FlagsObservationFetcher(
            fetcher_id="flags_of_1", at=DefinedDateTime.EFFECTIVE_DATETIME
        )
        flags_of_2 = FlagsObservationFetcher(fetcher_id="flags_of_1", at=DefinedDateTime.LIVE)
        self.assertNotEqual(flags_of_1, flags_of_2)

    def test_flags_observation_fetcher_unequal_by_filter(self):
        flags_of_1 = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
        )
        flags_of_2 = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["id1", "id3"]),
        )
        self.assertNotEqual(flags_of_1, flags_of_2)

    def test_flags_observation_fetcher_repr_with_filter(self):
        flags_of = FlagsObservationFetcher(
            fetcher_id="flags_of_1",
            at=DefinedDateTime.LIVE,
            filter=FlagsFilter(flag_definition_ids=["id1", "id2"]),
        )
        expected = (
            "FlagsObservationFetcher(fetcher_id='flags_of_1', at=DefinedDateTime.LIVE, "
            "filter=FlagsFilter(flag_definition_ids=['id1', 'id2']))"
        )
        self.assertEqual(expected, repr(flags_of))

    def test_flags_observation_fetcher_repr_filter_not_populated(self):
        flags_of = FlagsObservationFetcher(fetcher_id="flags_of_1", at=DefinedDateTime.LIVE)
        expected = (
            "FlagsObservationFetcher(fetcher_id='flags_of_1', at=DefinedDateTime.LIVE, filter=None)"
        )
        self.assertEqual(expected, repr(flags_of))

    def test_flags_observation_fetcher_fetcher_id_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsObservationFetcher(fetcher_id=1, at=DefinedDateTime.LIVE)
        self.assertEqual(
            str(e.exception),
            "'FlagsObservationFetcher.fetcher_id' expected str, got '1' of type int",
        )

    def test_flags_observation_fetcher_at_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsObservationFetcher(fetcher_id="flags_of_1", at=1)
        self.assertEqual(
            str(e.exception),
            (
                "'FlagsObservationFetcher.at' expected Union[DefinedDateTime, RelativeDateTime], "
                "got '1' of type int"
            ),
        )

    def test_flags_observation_fetcher_filter_wrong_type_raises_error(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsObservationFetcher(fetcher_id="flags_of_1", at=DefinedDateTime.LIVE, filter="hi")
        self.assertEqual(
            str(e.exception),
            (
                "'FlagsObservationFetcher.filter' expected FlagsFilter if populated, got 'hi' of "
                "type str"
            ),
        )

    def test_flags_observation_fetcher_raises_if_at_populated_with_interval_start(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsObservationFetcher(
                fetcher_id="fetcher_id",
                at=DefinedDateTime.INTERVAL_START,
            )
        self.assertEqual(
            str(e.exception),
            "FlagsObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )

    def test_flags_observation_fetcher_raises_if_at_origin_populated_with_interval_start(self):
        relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.INTERVAL_START, shift=Shift(months=-1)
        )
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsObservationFetcher(
                fetcher_id="fetcher_id",
                at=relative_date_time,
            )
        self.assertEqual(
            str(e.exception),
            "FlagsObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'",
        )



