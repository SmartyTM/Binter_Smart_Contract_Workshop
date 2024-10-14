from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from zoneinfo import ZoneInfo

from ..types import (
    Balance,
    BalanceCoordinate,
    
    ClientTransaction,
    DeactivationHookArguments,
    CustomInstruction,
    DEFAULT_ADDRESS,
    DEFAULT_ASSET,
    DerivedParameterHookArguments,
    InboundAuthorisation,
    InboundHardSettlement,
    Phase,
    ActivationHookArguments,
    Posting,
    PostParameterChangeHookArguments,
    PostPostingHookArguments,
    PreParameterChangeHookArguments,
    PrePostingHookArguments,
    ScheduleExpression,
    
    ScheduledEventHookArguments,
    ScheduledEvent,
    Settlement,
    SupervisorActivationHookArguments,
    SupervisorConversionHookArguments,
    SupervisorPostPostingHookArguments,
    SupervisorPrePostingHookArguments,
    SupervisorScheduledEventHookArguments,
    Timeline,
    TransactionCode,
    Transfer,
    Tside,
    ConversionHookArguments,
    
)
from ..types.postings import _PITypes_str
from .....utils.exceptions import (
    StrongTypingError,
    InvalidSmartContractError,
)
from .....utils import symbols



from .....utils.types_utils import (
    ContractsLanguageDunderMixin,
)


class PublicCommonV400HookArgumentsTypesTestCase(TestCase):
    test_naive_datetime = datetime(year=2021, month=1, day=1)
    test_zoned_datetime_utc = datetime(year=2021, month=1, day=1, tzinfo=ZoneInfo("UTC"))
    
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_id = "client_id"
        cls.account_id = "account_id"
        cls.client_transaction_id_custom = "client_transaction_id_custom"
        cls.client_transaction_id_settle = "client_transaction_id_settle"
        cls.client_transaction_id_transfer = "client_transaction_id_transfer"
        cls.posting_datetime = datetime(2022, 12, 12, tzinfo=ZoneInfo("UTC"))
        cls.custom_instruction = CustomInstruction(
            postings=[
                Posting(
                    credit=False,
                    amount=Decimal(10),
                    denomination="GBP",
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
            ],
            instruction_details={"TYPE": "PURCHASE"},
            transaction_code=TransactionCode(
                domain="something",
                family="other",
                subfamily="same",
            ),
        )
        cls.custom_instruction._set_output_attributes(  # noqa: SLF001
            insertion_datetime=cls.posting_datetime,
            value_datetime=cls.posting_datetime,
            client_batch_id="client_batch_id",
            batch_id="batch_id",
            committed_postings=[
                Posting(
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=False,
                    phase=Phase.COMMITTED,
                    amount=Decimal(10),
                    denomination="GBP",
                ),
            ],
            instruction_id="instruction_id_1",
            unique_client_transaction_id=f"{cls.client_id}_{cls.client_transaction_id_custom}",
            own_account_id=cls.account_id,
            tside=Tside.LIABILITY,
        )
        cls.inbound_auth = InboundAuthorisation(
            client_transaction_id=cls.client_transaction_id_settle,
            denomination="GBP",
            target_account_id=cls.account_id,
            amount=Decimal(20),
            internal_account_id="1",
        )
        cls.inbound_auth._set_output_attributes(  # noqa: SLF001
            insertion_datetime=cls.posting_datetime,
            value_datetime=cls.posting_datetime,
            client_batch_id="client_batch_id",
            batch_id="batch_id",
            committed_postings=[
                Posting(
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=True,
                    phase=Phase.PENDING_IN,
                    amount=Decimal(20),
                    denomination="GBP",
                ),
            ],
            instruction_id="instruction_id_4",
            unique_client_transaction_id=f"{cls.client_id}_{cls.client_transaction_id_settle}",
            own_account_id=cls.account_id,
            tside=Tside.LIABILITY,
        )
        cls.settlement = Settlement(client_transaction_id=cls.client_transaction_id_settle)
        cls.settlement._set_output_attributes(  # noqa: SLF001
            insertion_datetime=cls.posting_datetime,
            value_datetime=cls.posting_datetime,
            client_batch_id="client_batch_id",
            batch_id="batch_id",
            committed_postings=[
                Posting(
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=True,
                    phase=Phase.COMMITTED,
                    amount=Decimal(20),
                    denomination="GBP",
                ),
                Posting(
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=False,
                    phase=Phase.PENDING_IN,
                    amount=Decimal(20),
                    denomination="GBP",
                ),
            ],
            instruction_id="instruction_id_2",
            unique_client_transaction_id=f"{cls.client_id}_{cls.client_transaction_id_settle}",
            target_account_id=cls.account_id,
            own_account_id=cls.account_id,
            tside=Tside.LIABILITY,
        )
        cls.transfer = Transfer(
            creditor_target_account_id=cls.account_id,
            denomination="HKK",
            amount=Decimal(10),
            debtor_target_account_id="1",
        )
        cls.transfer._set_output_attributes(  # noqa: SLF001
            insertion_datetime=cls.posting_datetime,
            value_datetime=cls.posting_datetime,
            client_batch_id="client_batch_id",
            batch_id="batch_id",
            committed_postings=[
                Posting(
                    account_id=cls.account_id,
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=True,
                    phase=Phase.COMMITTED,
                    amount=Decimal(1),
                    denomination="HKK",
                ),
            ],
            instruction_id="instruction_id_3",
            unique_client_transaction_id=f"{cls.client_id}_{cls.client_transaction_id_transfer}",
            own_account_id=cls.account_id,
            tside=Tside.LIABILITY,
        )
        cls.hard_settle = InboundHardSettlement(
            denomination="GBP", target_account_id="123", amount=Decimal(20), internal_account_id="1"
        )
        cls.hard_settle._set_output_attributes(  # noqa: SLF001
            insertion_datetime=cls.posting_datetime,
            value_datetime=cls.posting_datetime,
            client_batch_id="client_batch_id",
            batch_id="batch_id",
            committed_postings=[
                Posting(
                    account_id="123",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    credit=True,
                    phase=Phase.COMMITTED,
                    amount=Decimal(20),
                    denomination="GBP",
                ),
            ],
            instruction_id="instruction_id_5",
            unique_client_transaction_id=f"{cls.client_id}_123",
            own_account_id="123",
            tside=Tside.ASSET,
        )

    # DeactivationHookArguments

    def test_deactivation_hook_arguments_repr(self):
        args = DeactivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        expected = (
            "DeactivationHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(args))

    def test_deactivation_hook_arguments_equality(self):
        args = DeactivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = DeactivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertEqual(args, other_args)

    def test_deactivation_hook_arguments_unequal_effective_datetime(self):
        args = DeactivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = DeactivationHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertNotEqual(args, other_args)

    def test_deactivation_hook_arguments_attributes_can_be_set(self):
        hook_args = DeactivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)

    def test_only_set_deactivation_hook_arguments_attributes_can_be_accessed(self):
        hook_args = DeactivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.__dict__, {"effective_datetime": self.test_zoned_datetime_utc})

    def test_deactivation_hook_arguments_attributes_not_set_cant_be_accessed(self):
        hook_args = DeactivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_deactivation_hook_arguments_spec(self):
        hook_args = DeactivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        public_attributes = hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001

        self.assertEqual(len(public_attributes), 1)
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual(effective_datetime_attribute.name, "effective_datetime")
        self.assertEqual(effective_datetime_attribute.type, "datetime")

    def test_deactivation_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DeactivationHookArguments(
                effective_datetime=self.test_naive_datetime,
            )
        expected = "'effective_datetime' of DeactivationHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_deactivation_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DeactivationHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'effective_datetime' of DeactivationHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # DerivedParameterHookArguments

    def test_derived_parameters_hook_arguments_repr(self):
        args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        expected = (
            "DerivedParameterHookArguments(effective_datetime="
            + "datetime.datetime(2021, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(args))

    def test_derived_parameters_arguments_attributes_can_be_set(self):
        hook_args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)

    def test_derived_parameter_hook_arguments_equality(self):
        args = DerivedParameterHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = DerivedParameterHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertEqual(args, other_args)

    def test_derived_parameter_hook_arguments_unequal_effective_datetime(self):
        args = DerivedParameterHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = DerivedParameterHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertNotEqual(args, other_args)

    def test_only_set_derived_parameters_arguments_attributes_can_be_accessed(self):
        hook_args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.__dict__, {"effective_datetime": self.test_zoned_datetime_utc})

    def test_derived_parameters_arguments_attributes_not_set_cant_be_accessed(self):
        hook_args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_derived_parameters_spec(self):
        hook_args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)

        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "DerivedParameterHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_derived_parameters_arguments_public_attributes(self):
        hook_args = DerivedParameterHookArguments(effective_datetime=self.test_zoned_datetime_utc)

        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        self.assertEqual(len(public_attributes), 1)
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual(effective_datetime_attribute.name, "effective_datetime")
        self.assertEqual(effective_datetime_attribute.type, "datetime")

    def test_derived_parameters_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DerivedParameterHookArguments(
                effective_datetime=self.test_naive_datetime,
            )
        expected = "'effective_datetime' of DerivedParameterHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_derived_parameters_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DerivedParameterHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'effective_datetime' of DerivedParameterHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # SupervisorActivationHookArguments

    def test_supevisor_activation_hook_arguments_repr(self):
        args = SupervisorActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        expected = (
            "SupervisorActivationHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(args))

    def test_supevisor_activation_hook_arguments_equality(self):
        args = SupervisorActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = SupervisorActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertEqual(args, other_args)

    def test_supevisor_activation_hook_arguments_unequal_effective_datetime(self):
        args = SupervisorActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = SupervisorActivationHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertNotEqual(args, other_args)

    def test_supervisor_activation_hook_arguments_attributes_can_be_set(self):
        hook_args = SupervisorActivationHookArguments(
            effective_datetime=self.test_zoned_datetime_utc
        )
        self.assertEqual(self.test_zoned_datetime_utc, hook_args.effective_datetime)

    def test_only_set_supervisor_activation_hook_arguments_attributes_can_be_accessed(self):
        hook_args = SupervisorActivationHookArguments(
            effective_datetime=self.test_zoned_datetime_utc
        )
        self.assertEqual({"effective_datetime": self.test_zoned_datetime_utc}, hook_args.__dict__)
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_supervisor_activation_hook_arguments_spec(self):
        hook_args = SupervisorActivationHookArguments(
            effective_datetime=self.test_zoned_datetime_utc
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }
        self.assertEqual("SupervisorActivationHookArguments", spec.name)
        self.assertEqual(public_attributes_dict.keys(), spec.public_attributes.keys())
        self.assertEqual(public_attributes_dict.keys(), spec.constructor.args.keys())
        self.assertEqual({}, spec.public_methods)

    def test_supervisor_activation_hook_arguments_public_attributes(self):
        hook_args = SupervisorActivationHookArguments(
            effective_datetime=self.test_zoned_datetime_utc
        )
        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        self.assertEqual(1, len(public_attributes))
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual("effective_datetime", effective_datetime_attribute.name)
        self.assertEqual("datetime", effective_datetime_attribute.type)

    def test_supervisor_activation_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorActivationHookArguments(
                effective_datetime=self.test_naive_datetime,
            )
        expected = (
            "'effective_datetime' of SupervisorActivationHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_activation_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorActivationHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'effective_datetime' of SupervisorActivationHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # SupervisorConversionHookArguments

    def test_supervisor_conversion_hook_arguments(self):
        hook_args = SupervisorConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            existing_schedules={
                "test_event": ScheduledEvent(
                    start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                    expression=ScheduleExpression(day="5"),
                ),
            },
        )
        expected = (
            "SupervisorConversionHookArguments(effective_datetime="
            + "datetime.datetime(2021, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "existing_schedules={'test_event': "
            + "ScheduledEvent(start_datetime=datetime.datetime(1970, 1, 1, 0, 0, 1, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), end_datetime=None, "
            + "expression=ScheduleExpression(day='5', day_of_week=None, hour=None, minute=None, "
            + "second=None, month=None, year=None), schedule_method=None, skip=False)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(hook_args))

    def test_supervisor_conversion_hook_arguments_attributes_can_be_set(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = SupervisorConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )
        self.assertEqual(self.test_zoned_datetime_utc, hook_args.effective_datetime)
        self.assertEqual(existing_schedules, hook_args.existing_schedules)

    def test_supervisor_conversion_hook_arguments_equality(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        args = SupervisorConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            existing_schedules=existing_schedules,
        )
        other_args = SupervisorConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            existing_schedules=existing_schedules,
        )
        self.assertEqual(args, other_args)

    def test_supervisor_conversion_hook_arguments_unequal_effective_datetime(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        args = SupervisorConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            existing_schedules=existing_schedules,
        )
        other_args = SupervisorConversionHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            existing_schedules=existing_schedules,
        )
        self.assertNotEqual(args, other_args)

    def test_only_set_supervisor_conversion_hook_arguments_attributes_can_be_accessed(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = SupervisorConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )
        self.assertEqual(
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "existing_schedules": existing_schedules,
            },
            hook_args.__dict__,
        )
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_supervisor_conversion_hook_arguments_spec(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = SupervisorConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual("SupervisorConversionHookArguments", spec.name)
        self.assertEqual(public_attributes_dict.keys(), spec.public_attributes.keys())
        self.assertEqual(public_attributes_dict.keys(), spec.constructor.args.keys())
        self.assertEqual({}, spec.public_methods)

    def test_supervisor_conversion_hook_arguments_public_attributes(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = SupervisorConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )

        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )
        self.assertEqual(2, len(public_attributes))
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual("effective_datetime", effective_datetime_attribute.name)
        self.assertEqual("datetime", effective_datetime_attribute.type)
        existing_schedules_attribute = public_attributes[1]
        self.assertEqual("existing_schedules", existing_schedules_attribute.name)
        self.assertEqual("Dict[str, ScheduledEvent]", existing_schedules_attribute.type)

    def test_supervisor_conversion_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorConversionHookArguments(
                effective_datetime=self.test_naive_datetime,
                existing_schedules={},
            )
        expected = (
            "'effective_datetime' of SupervisorConversionHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_conversion_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorConversionHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                existing_schedules={},
            )
        expected = "'effective_datetime' of SupervisorConversionHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # ActivationHookArguments

    def test_activation_hook_arguments_rerpr(self):
        args = ActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        expected = (
            "ActivationHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(args))

    def test_activation_hook_arguments_equality(self):
        args = ActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = ActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertEqual(args, other_args)

    def test_activation_hook_arguments_unequal_effective_datetime(self):
        args = ActivationHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        other_args = ActivationHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC"))
        )
        self.assertNotEqual(args, other_args)

    def test_post_activate_code_arguments_attributes_can_be_set(self):
        hook_args = ActivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)

    def test_only_set_post_activate_code_arguments_attributes_can_be_accessed(self):
        hook_args = ActivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.__dict__, {"effective_datetime": self.test_zoned_datetime_utc})

    def test_post_activate_code_arguments_attributes_not_set_cant_be_accessed(self):
        hook_args = ActivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_post_activate_code_spec(self):
        hook_args = ActivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)

        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "ActivationHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_post_activate_code_arguments_public_attributes(self):
        hook_args = ActivationHookArguments(effective_datetime=self.test_zoned_datetime_utc)

        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        self.assertEqual(len(public_attributes), 1)
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual(effective_datetime_attribute.name, "effective_datetime")
        self.assertEqual(effective_datetime_attribute.type, "datetime")

    def test_post_activate_code_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ActivationHookArguments(
                effective_datetime=self.test_naive_datetime,
            )
        expected = "'effective_datetime' of ActivationHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_post_activate_code_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ActivationHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'effective_datetime' of ActivationHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # ConversionHookArguments

    def test_conversion_hook_arguments_repr(self):
        args = ConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), existing_schedules={}
        )
        expected = (
            "ConversionHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), existing_schedules={})"
        )
        self.assertEqual(expected, repr(args))

    def test_conversion_hook_arguments_equality(self):
        args = ConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), existing_schedules={}
        )
        other_args = ConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), existing_schedules={}
        )
        self.assertEqual(args, other_args)

    def test_conversion_hook_arguments_unequal_effective_datetime(self):
        args = ConversionHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), existing_schedules={}
        )
        other_args = ConversionHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")), existing_schedules={}
        )
        self.assertNotEqual(args, other_args)

    def test_conversion_hook_arguments_attributes_can_be_set(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = ConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )
        self.assertEqual(self.test_zoned_datetime_utc, hook_args.effective_datetime)
        self.assertEqual(existing_schedules, hook_args.existing_schedules)

    def test_only_set_conversion_hook_arguments_attributes_can_be_accessed(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = ConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )
        self.assertEqual(
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "existing_schedules": existing_schedules,
            },
            hook_args.__dict__,
        )
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_conversion_hook_arguments_spec(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = ConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )

        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual("ConversionHookArguments", spec.name)
        self.assertEqual(public_attributes_dict.keys(), spec.public_attributes.keys())
        self.assertEqual(public_attributes_dict.keys(), spec.constructor.args.keys())
        self.assertEqual({}, spec.public_methods)

    def test_conversion_hook_arguments_public_attributes(self):
        existing_schedules = {
            "test_event": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
            ),
        }
        hook_args = ConversionHookArguments(
            effective_datetime=self.test_zoned_datetime_utc, existing_schedules=existing_schedules
        )

        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        self.assertEqual(2, len(public_attributes))
        effective_datetime_attribute = public_attributes[0]
        self.assertEqual("effective_datetime", effective_datetime_attribute.name)
        self.assertEqual("datetime", effective_datetime_attribute.type)
        existing_schedules_attribute = public_attributes[1]
        self.assertEqual("existing_schedules", existing_schedules_attribute.name)
        self.assertEqual("Dict[str, ScheduledEvent]", existing_schedules_attribute.type)

    def test_conversion_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ConversionHookArguments(
                effective_datetime=self.test_naive_datetime,
                existing_schedules={},
            )
        expected = "'effective_datetime' of ConversionHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_conversion_hook_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ConversionHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                existing_schedules={},
            )
        expected = "'effective_datetime' of ConversionHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # PostParameterChangeHookArguments

    def test_post_parameter_change_hook_arguments_repr(self):
        args = PostParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            old_parameter_values={},
            updated_parameter_values={},
        )
        expected = (
            "PostParameterChangeHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "old_parameter_values={}, updated_parameter_values={})"
        )
        self.assertEqual(expected, repr(args))

    def test_post_parameter_change_hook_arguments_equality(self):
        args = PostParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            old_parameter_values={},
            updated_parameter_values={},
        )
        other_args = PostParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            old_parameter_values={},
            updated_parameter_values={},
        )
        self.assertEqual(args, other_args)

    def test_post_parameter_change_hook_arguments_unequal_effective_datetime(self):
        args = PostParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            old_parameter_values={},
            updated_parameter_values={},
        )
        other_args = PostParameterChangeHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            old_parameter_values={},
            updated_parameter_values={},
        )
        self.assertNotEqual(args, other_args)

    def test_post_parameter_change_hook_arguments_attributes_can_be_set(self):
        old_parameter_values = {"param1": "old_val1", "param2": "old_val2"}
        updated_parameter_values = {"param1": "new_val1", "param2": "new_val2"}
        hook_args = PostParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            old_parameter_values=old_parameter_values,
            updated_parameter_values=updated_parameter_values,
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.old_parameter_values, old_parameter_values)
        self.assertEqual(hook_args.updated_parameter_values, updated_parameter_values)

    def test_only_set_post_parameter_change_hook_arguments_attributes_can_be_accessed(self):
        old_parameter_values = {"param1": "old_val1", "param2": "old_val2"}
        updated_parameter_values = {"param1": "new_val1", "param2": "new_val2"}
        hook_args = PostParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            old_parameter_values=old_parameter_values,
            updated_parameter_values=updated_parameter_values,
        )
        self.assertEqual(
            hook_args.__dict__,
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "old_parameter_values": old_parameter_values,
                "updated_parameter_values": updated_parameter_values,
            },
        )

    def test_post_parameter_change_hook_arguments_attributes_not_set_cant_be_accessed(self):
        old_parameter_values = {"param1": "old_val1", "param2": "old_val2"}
        updated_parameter_values = {"param1": "new_val1", "param2": "new_val2"}
        hook_args = PostParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            old_parameter_values=old_parameter_values,
            updated_parameter_values=updated_parameter_values,
        )
        self.assertRaises(AttributeError, getattr, hook_args, "postings")

    def test_post_parameter_change_hook_spec(self):
        old_parameter_values = {"param1": "old_val1", "param2": "old_val2"}
        updated_parameter_values = {"param1": "new_val1", "param2": "new_val2"}
        hook_args = PostParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            old_parameter_values=old_parameter_values,
            updated_parameter_values=updated_parameter_values,
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "PostParameterChangeHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_post_parameter_change_hook_arguments_public_attributes(self):
        old_parameter_values = {"param1": "old_val1", "param2": "old_val2"}
        updated_parameter_values = {"param1": "new_val1", "param2": "new_val2"}
        hook_args = PostParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            old_parameter_values=old_parameter_values,
            updated_parameter_values=updated_parameter_values,
        )
        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        self.assertEqual(len(public_attributes), 3)
        effective_datetime_attr, old_param_vals_attr, updated_param_vals_attr = public_attributes

        self.assertEqual(effective_datetime_attr.name, "effective_datetime")
        self.assertEqual(effective_datetime_attr.type, "datetime")

        self.assertEqual(old_param_vals_attr.name, "old_parameter_values")
        self.assertEqual(
            old_param_vals_attr.type,
            "Dict[str, Optional[Union[datetime, Decimal, int, OptionalValue, str, UnionItemValue]]]",
        )

        self.assertEqual(updated_param_vals_attr.name, "updated_parameter_values")
        self.assertEqual(
            updated_param_vals_attr.type,
            "Dict[str, Optional[Union[datetime, Decimal, int, OptionalValue, str, UnionItemValue]]]",
        )

    def test_post_parameter_change_hook_arguments_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PostParameterChangeHookArguments(
                effective_datetime=self.test_naive_datetime,
                old_parameter_values={},
                updated_parameter_values={},
            )
        expected = "'effective_datetime' of PostParameterChangeHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_post_parameter_change_arguments_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PostParameterChangeHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                old_parameter_values={},
                updated_parameter_values={},
            )
        expected = "'effective_datetime' of PostParameterChangeHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    # PostPostingHookArguments

    def test_post_posting_hook_arguments_repr(self):
        args = PostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        expected = (
            "PostPostingHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "posting_instructions=None, client_transactions={})"
        )
        self.assertEqual(expected, repr(args))

    def test_post_posting_hook_arguments_equality(self):
        args = PostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        other_args = PostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        self.assertEqual(args, other_args)

    def test_post_posting_hook_arguments_unequal_effective_datetime(self):
        args = PostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        other_args = PostPostingHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        self.assertNotEqual(args, other_args)

    def test_post_posting_hook_arguments_attributes_different_pi_types(self):
        custom_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_custom,
            account_id=self.account_id,
            posting_instructions=[self.custom_instruction],
            tside=Tside.LIABILITY,
        )
        settle_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_settle,
            account_id=self.account_id,
            posting_instructions=[self.inbound_auth, self.settlement],
            tside=Tside.LIABILITY,
        )
        transfer_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_transfer,
            account_id=self.account_id,
            posting_instructions=[self.transfer],
            tside=Tside.LIABILITY,
        )
        hook_args = PostPostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            posting_instructions=[self.custom_instruction, self.settlement, self.transfer],
            client_transactions={
                f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
            },
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(
            hook_args.posting_instructions,
            [self.custom_instruction, self.settlement, self.transfer],
        )
        # Check that balances() method on individual PIs
        self.assertEqual(
            hook_args.posting_instructions[0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.posting_instructions[1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.posting_instructions[1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(20), net=Decimal("-20")),
        )
        self.assertEqual(
            hook_args.posting_instructions[2].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        # Check that balances() method on individual ClientTransactions
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_custom}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0)),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_transfer}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )

    def test_post_posting_hook_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PostPostingHookArguments(
                effective_datetime=self.test_naive_datetime,
                posting_instructions=[],
                client_transactions={},
            )
        expected = "'effective_datetime' of PostPostingHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_post_posting_hook_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PostPostingHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                posting_instructions=[],
                client_transactions={},
            )
        expected = "'effective_datetime' of PostPostingHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_post_posting_hook_spec(self):
        hook_args = PostPostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            posting_instructions=[],
            client_transactions={},
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "PostPostingHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

        public_attributes = spec.public_attributes

        self.assertEqual(len(public_attributes), 3)
        effective_datetime, posting_instructions, client_transactions = public_attributes.values()

        self.assertEqual(effective_datetime.name, "effective_datetime")
        self.assertEqual(effective_datetime.type, "datetime")
        expected_docstring = """
                    The logical datetime that the hook is being run against. Must be a
                    timezone-aware UTC datetime using the ZoneInfo class. This datetime is equal to
                    the value timestamp of the posting instruction.
                """
        self.assertEqual(effective_datetime.docstring, expected_docstring)

        self.assertEqual(posting_instructions.name, "posting_instructions")
        self.assertEqual(posting_instructions.type, _PITypes_str)

        self.assertEqual(client_transactions.name, "client_transactions")
        self.assertEqual(client_transactions.type, "Dict[str, ClientTransaction]")

    # SupervisorPostPostingHookArguments

    def test_supervisor_post_posting_hook_arguments_repr(self):
        args = SupervisorPostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        expected = (
            "SupervisorPostPostingHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "supervisee_posting_instructions={}, supervisee_client_transactions={})"
        )
        self.assertEqual(expected, repr(args))

    def test_supervisor_post_posting_hook_arguments_equality(self):
        args = SupervisorPostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        other_args = SupervisorPostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        self.assertEqual(args, other_args)

    def test_supervisor_post_posting_hook_arguments_unequal_effective_datetime(self):
        args = SupervisorPostPostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        other_args = SupervisorPostPostingHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        self.assertNotEqual(args, other_args)

    def test_supervisor_post_posting_hook_arguments_attributes_can_be_set(self):
        custom_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_custom,
            account_id=self.account_id,
            posting_instructions=[self.custom_instruction],
            tside=Tside.LIABILITY,
        )
        settle_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_settle,
            account_id=self.account_id,
            posting_instructions=[self.inbound_auth, self.settlement],
            tside=Tside.LIABILITY,
        )
        transfer_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_transfer,
            account_id=self.account_id,
            posting_instructions=[self.transfer],
            tside=Tside.LIABILITY,
        )
        hard_settle_ctx = ClientTransaction(
            client_transaction_id="123",
            account_id="123",
            posting_instructions=[self.hard_settle],
            tside=Tside.ASSET,
        )
        hook_args = SupervisorPostPostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            supervisee_posting_instructions={
                self.account_id: [self.custom_instruction, self.settlement, self.transfer],
                "123": [self.hard_settle],
            },
            supervisee_client_transactions={
                self.account_id: {
                    f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                    f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                    f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
                },
                "123": {
                    f"{self.client_id}_123": hard_settle_ctx,
                },
            },
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(
            hook_args.supervisee_posting_instructions,
            {
                self.account_id: [self.custom_instruction, self.settlement, self.transfer],
                "123": [self.hard_settle],
            },
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions,
            {
                self.account_id: {
                    f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                    f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                    f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
                },
                "123": {
                    f"{self.client_id}_123": hard_settle_ctx,
                },
            },
        )
        # Check that balances() method on individual PIs for each supervisee
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(20), net=Decimal("-20")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][2].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions["123"][0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("-20")),
        )
        # Check that balances() method on individual ClientTransactions
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_custom}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0)),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_transfer}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions["123"][f"{self.client_id}_123"].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("-20")),
        )

    def test_supervisor_post_posting_hook_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorPostPostingHookArguments(
                effective_datetime=self.test_naive_datetime,
                supervisee_posting_instructions={},
                supervisee_client_transactions={},
            )
        expected = (
            "'effective_datetime' of SupervisorPostPostingHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_post_posting_hook_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorPostPostingHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                supervisee_posting_instructions={},
                supervisee_client_transactions={},
            )
        expected = "'effective_datetime' of SupervisorPostPostingHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_post_posting_hook_spec(self):
        hook_args = SupervisorPostPostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            supervisee_posting_instructions={},
            supervisee_client_transactions={},
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001

        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "SupervisorPostPostingHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

        public_attributes = spec.public_attributes

        self.assertEqual(len(public_attributes), 3)
        effective_datetime, postings, client_transactions = public_attributes.values()

        self.assertEqual(effective_datetime.name, "effective_datetime")
        self.assertEqual(effective_datetime.type, "datetime")

        self.assertEqual(postings.name, "supervisee_posting_instructions")
        self.assertEqual(postings.type, f"Dict[str, {_PITypes_str}]")

        self.assertEqual(client_transactions.name, "supervisee_client_transactions")
        self.assertEqual(client_transactions.type, "Dict[str, Dict[str, ClientTransaction]]")

    # PrePostingHookArguments

    def test_pre_posting_hook_arguments_repr(self):
        args = PrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        expected = (
            "PrePostingHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "posting_instructions=None, client_transactions={})"
        )
        self.assertEqual(expected, repr(args))

    def test_pre_posting_hook_arguments_equality(self):
        args = PrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        other_args = PrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        self.assertEqual(args, other_args)

    def test_pre_posting_hook_arguments_unequal_effective_datetime(self):
        args = PrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        other_args = PrePostingHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            posting_instructions=None,
            client_transactions={},
        )
        self.assertNotEqual(args, other_args)

    def test_pre_posting_hook_arguments_attributes_can_be_set(self):
        custom_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_custom,
            account_id=self.account_id,
            posting_instructions=[self.custom_instruction],
            tside=Tside.LIABILITY,
        )
        settle_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_settle,
            account_id=self.account_id,
            posting_instructions=[self.inbound_auth, self.settlement],
            tside=Tside.LIABILITY,
        )
        transfer_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_transfer,
            account_id=self.account_id,
            posting_instructions=[self.transfer],
            tside=Tside.LIABILITY,
        )
        hook_args = PrePostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            posting_instructions=[self.custom_instruction, self.settlement, self.transfer],
            client_transactions={
                f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
            },
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(
            hook_args.posting_instructions,
            [self.custom_instruction, self.settlement, self.transfer],
        )
        # Check that balances() method on individual PIs
        self.assertEqual(
            hook_args.posting_instructions[0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.posting_instructions[1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.posting_instructions[1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(20), net=Decimal("-20")),
        )
        self.assertEqual(
            hook_args.posting_instructions[2].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        # Check that balances() method on individual ClientTransactions
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_custom}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0)),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.client_transactions[
                f"{self.client_id}_{self.client_transaction_id_transfer}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )

    def test_pre_posting_hook_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PrePostingHookArguments(
                effective_datetime=self.test_naive_datetime,
                posting_instructions=[],
                client_transactions={},
            )
        expected = "'effective_datetime' of PrePostingHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_pre_posting_hook_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            PrePostingHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                posting_instructions=[],
                client_transactions={},
            )
        expected = "'effective_datetime' of PrePostingHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_pre_posting_hook_spec(self):
        hook_args = PrePostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            posting_instructions=[],
            client_transactions={},
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "PrePostingHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

        public_attributes = spec.public_attributes

        self.assertEqual(len(public_attributes), 3)
        effective_datetime, posting_instructions, client_transactions = public_attributes.values()

        self.assertEqual(effective_datetime.name, "effective_datetime")
        self.assertEqual(effective_datetime.type, "datetime")
        expected_docstring = """
                    The logical datetime that the hook is being run against. Must be a
                    timezone-aware UTC datetime using the ZoneInfo class. This datetime is equal to
                    the value timestamp of the posting instruction.
                """
        self.assertEqual(effective_datetime.docstring, expected_docstring)

        self.assertEqual(posting_instructions.name, "posting_instructions")
        self.assertEqual(posting_instructions.type, _PITypes_str)

        self.assertEqual(client_transactions.name, "client_transactions")
        self.assertEqual(client_transactions.type, "Dict[str, ClientTransaction]")

    # SupervisorPrePostingHookArguments

    def test_supervisor_pre_posting_hook_arguments_repr(self):
        args = SupervisorPrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        expected = (
            "SupervisorPrePostingHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "supervisee_posting_instructions={}, supervisee_client_transactions={})"
        )
        self.assertEqual(expected, repr(args))

    def test_supervisor_pre_posting_hook_arguments_equality(self):
        args = SupervisorPrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        other_args = SupervisorPrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        self.assertEqual(args, other_args)

    def test_supervisor_pre_posting_hook_arguments_unequal_effective_datetime(self):
        args = SupervisorPrePostingHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        other_args = SupervisorPrePostingHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            supervisee_client_transactions={},
            supervisee_posting_instructions={},
        )
        self.assertNotEqual(args, other_args)

    def test_supervisor_pre_posting_hook_arguments_attributes_can_be_set(self):
        custom_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_custom,
            account_id=self.account_id,
            posting_instructions=[self.custom_instruction],
            tside=Tside.LIABILITY,
        )
        settle_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_settle,
            account_id=self.account_id,
            posting_instructions=[self.inbound_auth, self.settlement],
            tside=Tside.LIABILITY,
        )
        transfer_ctx = ClientTransaction(
            client_transaction_id=self.client_transaction_id_transfer,
            account_id=self.account_id,
            posting_instructions=[self.transfer],
            tside=Tside.LIABILITY,
        )
        hard_settle_ctx = ClientTransaction(
            client_transaction_id="123",
            account_id="123",
            posting_instructions=[self.hard_settle],
            tside=Tside.ASSET,
        )
        hook_args = SupervisorPrePostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            supervisee_posting_instructions={
                self.account_id: [self.custom_instruction, self.settlement, self.transfer],
                "123": [self.hard_settle],
            },
            supervisee_client_transactions={
                self.account_id: {
                    f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                    f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                    f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
                },
                "123": {
                    f"{self.client_id}_123": hard_settle_ctx,
                },
            },
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(
            hook_args.supervisee_posting_instructions,
            {
                self.account_id: [self.custom_instruction, self.settlement, self.transfer],
                "123": [self.hard_settle],
            },
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions,
            {
                self.account_id: {
                    f"{self.client_id}_{self.client_transaction_id_custom}": custom_ctx,
                    f"{self.client_id}_{self.client_transaction_id_settle}": settle_ctx,
                    f"{self.client_id}_{self.client_transaction_id_transfer}": transfer_ctx,
                },
                "123": {
                    f"{self.client_id}_123": hard_settle_ctx,
                },
            },
        )
        # Check that balances() method on individual PIs for each supervisee
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][1].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(20), net=Decimal("-20")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions[self.account_id][2].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        self.assertEqual(
            hook_args.supervisee_posting_instructions["123"][0].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("-20")),
        )
        # Check that balances() method on individual ClientTransactions
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_custom}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(0), debit=Decimal(10), net=Decimal("-10")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.PENDING_IN,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0)),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_settle}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("20")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions[self.account_id][
                f"{self.client_id}_{self.client_transaction_id_transfer}"
            ].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="HKK",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(1), debit=Decimal(0), net=Decimal("1")),
        )
        self.assertEqual(
            hook_args.supervisee_client_transactions["123"][f"{self.client_id}_123"].balances()[
                BalanceCoordinate(
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    denomination="GBP",
                    phase=Phase.COMMITTED,
                )
            ],
            Balance(credit=Decimal(20), debit=Decimal(0), net=Decimal("-20")),
        )

    def test_supervisor_pre_posting_hook_raises_with_naive_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorPrePostingHookArguments(
                effective_datetime=self.test_naive_datetime,
                supervisee_posting_instructions={},
                supervisee_client_transactions={},
            )
        expected = (
            "'effective_datetime' of SupervisorPrePostingHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_pre_posting_hook_raises_with_non_utc_effective_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorPrePostingHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                supervisee_posting_instructions={},
                supervisee_client_transactions={},
            )
        expected = "'effective_datetime' of SupervisorPrePostingHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_pre_posting_hook_spec(self):
        hook_args = SupervisorPrePostingHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            supervisee_posting_instructions={},
            supervisee_client_transactions={},
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "SupervisorPrePostingHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

        public_attributes = spec.public_attributes

        self.assertEqual(len(public_attributes), 3)
        effective_datetime, postings, client_transactions = public_attributes.values()

        self.assertEqual(effective_datetime.name, "effective_datetime")
        self.assertEqual(effective_datetime.type, "datetime")

        self.assertEqual(postings.name, "supervisee_posting_instructions")
        self.assertEqual(postings.type, f"Dict[str, {_PITypes_str}]")

        self.assertEqual(client_transactions.name, "supervisee_client_transactions")
        self.assertEqual(client_transactions.type, "Dict[str, Dict[str, ClientTransaction]]")

    # PreParameterChangeHookArguments

    def test_pre_parameter_change_hook_arguments_repr(self):
        args = PreParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            updated_parameter_values={},
        )
        expected = (
            "PreParameterChangeHookArguments(effective_datetime="
            + "datetime.datetime(2012, 12, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "updated_parameter_values={}, effective_in=Timeline.PRESENT, is_cancellation=False)"
        )
        self.assertEqual(expected, repr(args))

    def test_pre_parameter_change_hook_arguments_equality(self):
        args = PreParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            updated_parameter_values={},
        )
        other_args = PreParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            updated_parameter_values={},
        )
        self.assertEqual(args, other_args)

    def test_pre_parameter_change_hook_arguments_unequal_effective_datetime(self):
        args = PreParameterChangeHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            updated_parameter_values={},
        )
        other_args = PreParameterChangeHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            updated_parameter_values={},
        )
        self.assertNotEqual(args, other_args)

    def test_pre_parameter_change_hook_arguments_attributes_can_be_set(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.updated_parameter_values, parameters)

    def test_pre_parameter_change_hook_raises_with_naive_effective_datetime(self):
        parameters = {"parameter1": "value1"}
        with self.assertRaises(InvalidSmartContractError) as ex:
            PreParameterChangeHookArguments(
                effective_datetime=self.test_naive_datetime,
                updated_parameter_values=parameters,
            )
        expected = "'effective_datetime' of PreParameterChangeHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_pre_parameter_change_hook_raises_with_non_utc_effective_datetime(self):
        parameters = {"parameter1": "value1"}
        with self.assertRaises(InvalidSmartContractError) as ex:
            PreParameterChangeHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                updated_parameter_values=parameters,
            )
        expected = "'effective_datetime' of PreParameterChangeHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_pre_parameter_change_hook_arguments_attributes(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
            effective_in=Timeline.FUTURE,
            is_cancellation=True,
        )
        self.assertEqual(
            hook_args.__dict__,
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "updated_parameter_values": parameters,
                "effective_in": Timeline.FUTURE,
                "is_cancellation": True,
            },
        )

    def test_set_pre_parameter_change_hook_arguments_attributes_with_default_values(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
        )
        self.assertEqual(
            hook_args.__dict__,
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "updated_parameter_values": parameters,
                "effective_in": Timeline.PRESENT,
                "is_cancellation": False,
            },
        )

    def test_pre_parameter_change_hook_arguments_unknown_attributes_cant_be_accessed(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
        )
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_pre_parameter_change_hook_spec(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "PreParameterChangeHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_pre_parameter_change_hook_arguments_public_attributes(self):
        parameters = {"parameter1": "value1"}
        hook_args = PreParameterChangeHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            updated_parameter_values=parameters,
        )
        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        (
            effective_datetime_attr,
            parameters_attr,
            effective_in_attr,
            is_cancellation_attr,
        ) = public_attributes

        self.assertEqual(effective_datetime_attr.name, "effective_datetime")
        self.assertEqual(effective_datetime_attr.type, "datetime")

        self.assertEqual(parameters_attr.name, "updated_parameter_values")
        self.assertEqual(
            parameters_attr.type,
            "Dict[str, Optional[Union[datetime, Decimal, int, OptionalValue, str, UnionItemValue]]]",
        )

        self.assertEqual(effective_in_attr.name, "effective_in")
        self.assertEqual(effective_in_attr.type, "Timeline")

        self.assertEqual(is_cancellation_attr.name, "is_cancellation")
        self.assertEqual(is_cancellation_attr.type, "bool")

    # ScheduledEventHookArguments

    def test_scheduled_event_hook_arguments_repr(self):
        args = ScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type="test_event",
        )
        self.assertTrue(issubclass(ScheduledEventHookArguments, ContractsLanguageDunderMixin))
        self.assertIn("ScheduledEventHookArguments", repr(args))

    def test_scheduled_event_hook_arguments_equality(self):
        event_type = "test_event"
        args = ScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), event_type=event_type
        )
        other_args = ScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), event_type=event_type
        )
        self.assertEqual(args, other_args)

    def test_scheduled_event_hook_arguments_unequal_effective_datetime(self):
        event_type = "test_event"
        args = ScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")), event_type=event_type
        )
        other_args = ScheduledEventHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")), event_type=event_type
        )
        self.assertNotEqual(args, other_args)

    def test_scheduled_event_hook_arguments_attributes_can_be_set(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        hook_args = ScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            pause_at_datetime=pause_at_datetime,
            
        )
        self.assertEqual(hook_args.effective_datetime, self.test_zoned_datetime_utc)
        self.assertEqual(hook_args.event_type, event_type)
        self.assertEqual(hook_args.pause_at_datetime, pause_at_datetime)
        

    def test_scheduled_event_hook_arguments_raises_with_naive_effective_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEventHookArguments(
                effective_datetime=self.test_naive_datetime,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
            )
        expected = "'effective_datetime' of ScheduledEventHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_non_utc_effective_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEventHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
            )
        expected = "'effective_datetime' of ScheduledEventHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_naive_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12)
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
            )
        expected = "'pause_at_datetime' of ScheduledEventHookArguments is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_non_utc_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("US/Pacific"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
            )
        expected = "'pause_at_datetime' of ScheduledEventHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_incorrect_pause_at_datetime_type(self):
        event_type = "test_event"
        with self.assertRaises(StrongTypingError) as ex:
            ScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=False,
            )
        expected = "'pause_at_datetime' expected datetime, got 'False' of type bool"  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_only_set_scheduled_event_hook_arguments_attributes_can_be_accessed(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        hook_args = ScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            pause_at_datetime=pause_at_datetime,
            
        )
        self.assertEqual(
            hook_args.__dict__,
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "event_type": event_type,
                "pause_at_datetime": pause_at_datetime,
                
            },
        )

    def test_scheduled_event_hook_arguments_attributes_not_set_cant_be_accessed(self):
        event_type = "test_event"
        hook_args = ScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
        )
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_scheduled_event_hook_spec(self):
        event_type = "test_event"
        hook_args = ScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            pause_at_datetime=datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC")),
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "ScheduledEventHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_scheduled_event_hook_arguments_public_attributes(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        hook_args = ScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            pause_at_datetime=pause_at_datetime,
        )
        public_attributes = iter(
            hook_args._public_attributes(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        )

        effective_datetime_attr = next(public_attributes)
        event_type_attr = next(public_attributes)
        scheduled_job_attr = next(public_attributes)

        self.assertEqual(effective_datetime_attr.name, "effective_datetime")
        self.assertEqual(effective_datetime_attr.type, "datetime")

        self.assertEqual(event_type_attr.name, "event_type")
        self.assertEqual(event_type_attr.type, "str")

        self.assertEqual(scheduled_job_attr.name, "pause_at_datetime")
        self.assertEqual(scheduled_job_attr.type, "Optional[datetime]")

        

    # SupervisorScheduledEventHookArguments

    def test_supervisor_scheduled_event_hook_arguments_repr(self):
        args = SupervisorScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type="test_event",
            supervisee_pause_at_datetime={},
        )
        self.assertTrue(
            issubclass(SupervisorScheduledEventHookArguments, ContractsLanguageDunderMixin),
        )
        self.assertIn("SupervisorScheduledEventHookArguments", repr(args))

    def test_supervisor_scheduled_event_hook_arguments_equality(self):
        event_type = "test_event"
        args = SupervisorScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type=event_type,
            supervisee_pause_at_datetime={},
        )
        other_args = SupervisorScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type=event_type,
            supervisee_pause_at_datetime={},
        )
        self.assertEqual(args, other_args)

    def test_supervisor_scheduled_event_hook_arguments_unequal_effective_datetime(self):
        event_type = "test_event"
        args = SupervisorScheduledEventHookArguments(
            effective_datetime=datetime(2012, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type=event_type,
            supervisee_pause_at_datetime={},
        )
        other_args = SupervisorScheduledEventHookArguments(
            effective_datetime=datetime(1984, 12, 12, tzinfo=ZoneInfo("UTC")),
            event_type=event_type,
            supervisee_pause_at_datetime={},
        )
        self.assertNotEqual(args, other_args)

    def test_supervisor_scheduled_event_hook_arguments_attributes_can_be_set(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        supervisee_pause_at_datetime = {"supervisee_account_id": pause_at_datetime}
        hook_args = SupervisorScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            supervisee_pause_at_datetime=supervisee_pause_at_datetime,
            pause_at_datetime=pause_at_datetime,
            
        )
        self.assertEqual(self.test_zoned_datetime_utc, hook_args.effective_datetime)
        self.assertEqual(event_type, hook_args.event_type)
        self.assertEqual(
            datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC")), hook_args.pause_at_datetime
        )
        self.assertEqual(supervisee_pause_at_datetime, hook_args.supervisee_pause_at_datetime)
        

    def test_supervisor_scheduled_event_hook_arguments_raises_with_naive_effective_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_naive_datetime,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime={},
                
            )
        expected = (
            "'effective_datetime' of SupervisorScheduledEventHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_scheduled_event_hook_arguments_raises_with_non_datetime_pause_at_datetime(
        self,
    ):
        event_type = "test_event"
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=False,
                supervisee_pause_at_datetime={},
                
            )
        expected = "'pause_at_datetime' expected datetime, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_scheduled_eventhook_arguments_raises_with_non_utc_effective_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_naive_datetime.replace(tzinfo=ZoneInfo("US/Pacific")),
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime={},
                
            )
        expected = "'effective_datetime' of SupervisorScheduledEventHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_scheduled_event_hook_arguments_raises_with_naive_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12)
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime={},
                
            )
        expected = (
            "'pause_at_datetime' of SupervisorScheduledEventHookArguments is not timezone aware."
        )
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_scheduled_event_hook_arguments_raises_with_non_utc_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("US/Pacific"))
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime={},
                
            )
        expected = "'pause_at_datetime' of SupervisorScheduledEventHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_naive_supervisee_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        naive_pause_at_datetime = datetime(2022, 10, 12)
        supervisee_pause_at_datetime = {
            "supervisee_account_id": pause_at_datetime,
            "supervisee_account_id_naive": naive_pause_at_datetime,
        }
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime=supervisee_pause_at_datetime,
                
            )
        expected = "'supervisee_pause_at_datetime['supervisee_account_id_naive']' of SupervisorScheduledEventHookArguments is not timezone aware."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_incorrect_supervisee_pause_at_datetime_type(
        self,
    ):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        not_a_datetime = False
        supervisee_pause_at_datetime = {
            "supervisee_account_id": pause_at_datetime,
            "supervisee_account_id_wrong_type": not_a_datetime,
        }
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime=supervisee_pause_at_datetime,
                
            )
        expected = "'supervisee_pause_at_datetime['supervisee_account_id_wrong_type']' expected datetime, got 'False' of type bool"  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_scheduled_event_hook_arguments_raises_with_non_utc_supervisee_pause_at_datetime(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        non_utc_pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("US/Pacific"))
        supervisee_pause_at_datetime = {
            "supervisee_account_id": pause_at_datetime,
            "supervisee_account_id_naive": non_utc_pause_at_datetime,
        }
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorScheduledEventHookArguments(
                effective_datetime=self.test_zoned_datetime_utc,
                event_type=event_type,
                pause_at_datetime=pause_at_datetime,
                supervisee_pause_at_datetime=supervisee_pause_at_datetime,
                
            )
        expected = "'supervisee_pause_at_datetime['supervisee_account_id_naive']' of SupervisorScheduledEventHookArguments must have timezone UTC, currently US/Pacific."  # noqa: E501
        self.assertEqual(expected, str(ex.exception))

    def test_only_set_supervisor_scheduled_event_hook_arguments_attributes_can_be_accessed(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        supervisee_pause_at_datetime = {"supervisee_account_id": pause_at_datetime}
        hook_args = SupervisorScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            supervisee_pause_at_datetime=supervisee_pause_at_datetime,
            pause_at_datetime=pause_at_datetime,
            
        )
        self.assertEqual(
            hook_args.__dict__,
            {
                "effective_datetime": self.test_zoned_datetime_utc,
                "event_type": event_type,
                "supervisee_pause_at_datetime": supervisee_pause_at_datetime,
                "pause_at_datetime": pause_at_datetime,
                
            },
        )

    def test_supervisor_scheduled_event_hook_arguments_attributes_not_set_cant_be_accessed(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        supervisee_pause_at_datetime = {"supervisee_account_id": pause_at_datetime}
        hook_args = SupervisorScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            supervisee_pause_at_datetime=supervisee_pause_at_datetime,
            pause_at_datetime=pause_at_datetime,
            
        )
        self.assertRaises(AttributeError, getattr, hook_args, "old_parameter_values")

    def test_supervisor_scheduled_event_hook_spec(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        supervisee_pause_at_datetime = {"supervisee_account_id": pause_at_datetime}
        hook_args = SupervisorScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            supervisee_pause_at_datetime=supervisee_pause_at_datetime,
            pause_at_datetime=pause_at_datetime,
            
        )
        spec = hook_args._spec(language_code=symbols.Languages.ENGLISH)  # noqa: SLF001
        public_attributes_dict = {
            attribute.name: attribute
            for attribute in hook_args._public_attributes(symbols.Languages.ENGLISH)  # noqa: SLF001
        }

        self.assertEqual(spec.name, "SupervisorScheduledEventHookArguments")
        self.assertEqual(spec.public_attributes.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.constructor.args.keys(), public_attributes_dict.keys())
        self.assertEqual(spec.public_methods, {})

    def test_supervisor_scheduled_event_hook_arguments_public_attributes(self):
        event_type = "test_event"
        pause_at_datetime = datetime(2022, 10, 12, tzinfo=ZoneInfo("UTC"))
        supervisee_pause_at_datetime = {"supervisee_account_id": pause_at_datetime}
        hook_args = SupervisorScheduledEventHookArguments(
            effective_datetime=self.test_zoned_datetime_utc,
            event_type=event_type,
            supervisee_pause_at_datetime=supervisee_pause_at_datetime,
            pause_at_datetime=pause_at_datetime,
            
        )
        public_attributes = hook_args._public_attributes(  # noqa: SLF001
            language_code=symbols.Languages.ENGLISH
        )

        (
            effective_datetime_attr,
            event_type_attr,
            pause_at_datetime_attr,
            supervisee_pause_at_datetime_attr,
            
        ) = public_attributes

        self.assertEqual(effective_datetime_attr.name, "effective_datetime")
        self.assertEqual(effective_datetime_attr.type, "datetime")

        self.assertEqual(event_type_attr.name, "event_type")
        self.assertEqual(event_type_attr.type, "str")

        self.assertEqual(supervisee_pause_at_datetime_attr.name, "supervisee_pause_at_datetime")
        self.assertEqual(supervisee_pause_at_datetime_attr.type, "Dict[str, Optional[datetime]]")

        self.assertEqual(pause_at_datetime_attr.name, "pause_at_datetime")
        self.assertEqual(pause_at_datetime_attr.type, "Optional[datetime]")

        

    
    
