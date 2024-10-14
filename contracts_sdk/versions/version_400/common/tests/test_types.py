from collections import defaultdict
from unittest import TestCase
from copy import deepcopy
from datetime import datetime, timezone
from contextlib import redirect_stderr
from decimal import Decimal
from io import StringIO
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfo

from ..types import (
    AccountConstraint,
    AccountIdShape,
    AddressDetails,
    
    AccountNotificationDirective,
    ActivationHookResult,
    Balance,
    BalanceCoordinate,
    BalanceDefaultDict,
    BalancesFilter,
    BalancesObservation,
    CalendarEvent,
    CalendarEvents,
    CustomInstruction,
    DateShape,
    DateTimeConstraint,
    DateTimePrecision,
    DeactivationHookResult,
    DecimalConstraint,
    DEFAULT_ADDRESS,
    DEFAULT_ASSET,
    DefinedDateTime,
    DenominationShape,
    DerivedParameterHookResult,
    EndOfMonthSchedule,
    EnumerationConstraint,
    EventTypesGroup,
    ExpectedParameter,
    fetch_account_data,
    
    FlagsFilter,
    FlagsObservation,
    Logger,
    Next,
    NumberShape,
    OptionalShape,
    OptionalValue,
    Override,
    Parameter,
    ParameterLevel,
    ParametersFilter,
    ParametersObservation,
    Phase,
    PlanNotificationDirective,
    Posting,
    PostingInstructionsDirective,
    
    PostingInstructionRejectionReason,
    PostingInstructionType,
    PostParameterChangeHookResult,
    PreParameterChangeHookResult,
    
    PostPostingHookResult,
    PrePostingHookResult,
    Previous,
    Rejection,
    RejectionReason,
    RelativeDateTime,
    requires,
    ScheduleExpression,
    ScheduledEvent,
    
    ScheduledEventHookResult,
    ScheduleFailover,
    ScheduleSkip,
    Shift,
    SmartContractDescriptor,
    SmartContractEventType,
    StringConstraint,
    StringShape,
    SupervisedHooks,
    SupervisionExecutionMode,
    SupervisorActivationHookResult,
    SupervisorConversionHookResult,
    SupervisorContractEventType,
    SupervisorPostPostingHookResult,
    SupervisorPrePostingHookResult,
    SupervisorScheduledEventHookResult,
    Timeline,
    Tside,
    UnionItem,
    UnionItemValue,
    UnionShape,
    UpdateAccountEventTypeDirective,
    UpdatePlanEventTypeDirective,
    ParameterUpdatePermission,
    ConversionHookResult,
    AttributeHookResult,
    
)

from ..types import hook_results
from ..types.hook_results import (
    validate_account_directives,
    validate_supervisee_directives,
    validate_servicing_hook_directives,
)

from .....utils import symbols
from .....utils.exceptions import (
    StrongTypingError,
    InvalidSmartContractError,
)
from .....utils.feature_flags import (
    is_fflag_enabled,
    skip_if_not_enabled,
    ACCOUNT_ATTRIBUTE_HOOK,
    
    
    EXPECTED_PID_REJECTIONS,
    
    
)
from .....utils.types_utils import (
    ContractsLanguageDunderMixin,
)


class PublicCommonV400TypesTestCase(TestCase):
    test_account_id = "test_test_account_id"
    test_posting_instructions = [
        CustomInstruction(
            postings=[
                Posting(
                    amount=Decimal(1),
                    credit=True,
                    account_id="1",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
                Posting(
                    amount=Decimal(1),
                    credit=False,
                    account_id="2",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
            ],
        )
    ]
    test_account_notification_directives = [
        AccountNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value1"},
        )
    ]
    test_scheduled_events_return_value = {
        "event_1": ScheduledEvent(
            start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(1970, 1, 1, second=2, tzinfo=ZoneInfo("UTC")),
            expression=ScheduleExpression(
                year="2000",
                month="1",
                day="1",
                hour="0",
                minute="0",
                second="0",
            ),
            skip=ScheduleSkip(
                end=datetime(1970, 1, 1, second=4, tzinfo=ZoneInfo("UTC")),
            ),
        ),
        "event_2": ScheduledEvent(
            start_datetime=datetime(1970, 1, 1, second=5, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(1970, 1, 1, second=6, tzinfo=ZoneInfo("UTC")),
            expression=ScheduleExpression(
                day_of_week="mon",
            ),
        ),
    }
    test_posting_instructions_directives = [
        PostingInstructionsDirective(
            client_batch_id="international-payment",
            value_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            posting_instructions=test_posting_instructions,
        )
    ]
    test_posting_instructions_directive_with_rejection_reasons = PostingInstructionsDirective(
        client_batch_id="international-payment",
        value_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
        posting_instructions=test_posting_instructions,
        non_blocking_rejection_reasons={
            PostingInstructionRejectionReason.INSUFFICIENT_FUNDS,
            PostingInstructionRejectionReason.ACCOUNT_STATUS_INVALID,
        },
    )
    test_scheduled_events_return_value = {
        "event_1": ScheduledEvent(
            start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(1970, 1, 1, second=2, tzinfo=ZoneInfo("UTC")),
            expression=ScheduleExpression(
                year="2000",
                month="1",
                day="1",
                hour="0",
                minute="0",
                second="0",
            ),
            skip=ScheduleSkip(
                end=datetime(1970, 1, 1, second=3, tzinfo=ZoneInfo("UTC")),
            ),
        ),
        "event_2": ScheduledEvent(
            start_datetime=datetime(1970, 1, 1, second=5, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(1970, 1, 1, second=6, tzinfo=ZoneInfo("UTC")),
            expression=ScheduleExpression(
                day_of_week="mon",
            ),
        ),
    }
    test_update_account_event_type_directives = [
        UpdateAccountEventTypeDirective(
            event_type="event_type_1",
            end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
        )
    ]
    test_plan_notification_directives = [
        PlanNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value1"},
        )
    ]
    test_update_plan_event_type_directives = [
        UpdatePlanEventTypeDirective(
            event_type="event_type",
            skip=True,
        )
    ]
    test_supervisee_account_notification_directives = {
        test_account_id: [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
    }
    test_supervisee_posting_instructions_directives = {
        test_account_id: test_posting_instructions_directives
    }
    test_supervisee_update_account_event_type_directives = {
        test_account_id: [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
    }

    

    # Parameters

    def test_parameter(self):
        parameter = Parameter(
            name="day_of_month",
            description="Which day would you like interest to be paid?",
            display_name="Day of month to pay interest",
            level=ParameterLevel.GLOBAL,
            default_value=27,
            derived=False,
            shape=NumberShape(min_value=1, max_value=28, step=1),
        )
        self.assertEqual(parameter.default_value, 27)

    def test_parameter_init_validation(self):
        with self.assertRaises(TypeError) as ex:
            Parameter()
        self.assertEqual(
            str(ex.exception),
            "Parameter.__init__() missing 3 required keyword-only arguments: 'name', 'shape', and "
            "'level'",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name=None, shape=None, level=None)
        self.assertEqual(str(ex.exception), "Parameter attribute 'name' expected str, got None")

        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(name="", shape=StringShape(), level=1)
        self.assertEqual(str(ex.exception), "Parameter attribute 'name' must be a non-empty string")

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=None, level=None)
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'shape' expected Union[AccountIdShape, DateShape, "
            "DenominationShape, NumberShape, OptionalShape, StringShape, UnionShape],"
            " got None",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=Decimal, level=None)
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'shape' expected Union[AccountIdShape, DateShape, "
            "DenominationShape, NumberShape, OptionalShape, StringShape, UnionShape], got "
            "'<class 'decimal.Decimal'>'",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=StringShape, level=None)
        self.assertEqual(
            str(ex.exception),
            "Parameter init arg 'shape' for parameter 'name' must be an instance of the "
            "StringShape class",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=StringShape(), level=None)
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'level' expected ParameterLevel, got None",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=StringShape(), level=1.0)
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'level' expected ParameterLevel, got '1.0' of type float",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(name="name", shape=StringShape(), level=ParameterLevel.INSTANCE, derived=1)
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'derived' expected bool if populated, got '1' of type int",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="name",
                shape=StringShape(),
                level=ParameterLevel.INSTANCE,
                derived=True,
                display_name=True,
            )
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'display_name' expected str if populated, got 'True' of type bool",
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="name",
                shape=StringShape(),
                level=ParameterLevel.INSTANCE,
                derived=True,
                display_name="display_name",
                description=StringShape(),
            )
        self.assertEqual(
            str(ex.exception),
            (
                "Parameter attribute 'description' expected str if populated, "
                + "got 'StringShape()' of type StringShape"
            ),
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="name",
                shape=StringShape(),
                level=ParameterLevel.INSTANCE,
                derived=True,
                display_name="display_name",
                description="description",
                default_value=StringShape(),
            )
        expected = (
            "Parameter attribute 'default_value' expected Union[Decimal, str, "
            + "datetime, OptionalValue, UnionItemValue, int] if populated, "
            + "got 'StringShape()' of type StringShape"
        )
        self.assertEqual(expected, str(ex.exception))

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="name",
                shape=OptionalShape(shape=StringShape()),
                level=ParameterLevel.INSTANCE,
                derived=False,
                display_name="display_name",
                description="description",
                default_value=OptionalValue(Decimal(1)),
                update_permission=True,
            )
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'update_permission' expected ParameterUpdatePermission if "
            "populated, got 'True' of type bool",
        )

    def test_parameter_cannot_use_optional_default_value(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(
                name="overdraft_limit",
                level=ParameterLevel.TEMPLATE,
                description="Overdraft limit",
                shape=StringShape(),
                default_value=OptionalValue(1),
            )
        self.assertEqual(
            "Non optional shapes must have a non optional default value: overdraft_limit",
            str(ex.exception),
        )

    def test_parameter_invalid_default_value_raises_error(self):
        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="overdraft_limit",
                level=ParameterLevel.TEMPLATE,
                description="Overdraft limit",
                shape=StringShape(),
                default_value=500,
            )
        self.assertEqual(
            "Expected str, got '500' of type int",
            str(ex.exception),
        )

    def test_parameter_invalid_optional_default_value_raises_error(self):
        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="overdraft_limit",
                level=ParameterLevel.TEMPLATE,
                description="Overdraft limit",
                shape=OptionalShape(shape=StringShape()),
                default_value=500,
            )
        self.assertEqual(
            "Expected OptionalValue, got '500' of type int",
            str(ex.exception),
        )

        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="overdraft_limit",
                level=ParameterLevel.TEMPLATE,
                description="Overdraft limit",
                shape=OptionalShape(shape=StringShape()),
                default_value=OptionalValue(500),
            )
        self.assertEqual(
            "Expected str, got '500' of type int",
            str(ex.exception),
        )

    def test_optional_value_raises_with_invalid_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            OptionalValue(value=True)
        self.assertEqual(
            "'OptionalValue.value' expected Union[Decimal, str, datetime, UnionItemValue, int] "
            + "if populated, got 'True' of type bool",
            str(ex.exception),
        )

    def test_optional_value_raises_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            OptionalValue(datetime(2022, 1, 1))
        self.assertEqual(
            "'value' of OptionalValue is not timezone aware.",
            str(ex.exception),
        )

    def test_optional_value_raises_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            OptionalValue(datetime(2022, 1, 1, tzinfo=ZoneInfo("US/Pacific")))
        self.assertEqual(
            "'value' of OptionalValue must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_optional_value_raises_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            OptionalValue(datetime.fromtimestamp(1, timezone.utc))
        self.assertEqual(
            "'value' of OptionalValue must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_parameter_global_level(self):
        parameter = Parameter(
            name="day_of_month",
            description="Which day would you like interest to be paid?",
            display_name="Day of month to pay interest",
            level=ParameterLevel.GLOBAL,
            default_value=27,
            shape=NumberShape(min_value=1, max_value=28, step=1),
        )
        self.assertEqual(parameter.default_value, 27)

    def test_parameter_default_value_raises_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                default_value=datetime(2022, 1, 1),
                shape=DateShape(
                    min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                    max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
                ),
            )
        self.assertEqual(
            "'default_value' of Parameter is not timezone aware.",
            str(ex.exception),
        )

    def test_parameter_default_value_raises_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                default_value=datetime(2022, 1, 1, tzinfo=ZoneInfo("US/Pacific")),
                shape=DateShape(
                    min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                    max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
                ),
            )
        self.assertEqual(
            "'default_value' of Parameter must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_parameter_default_value_raises_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                default_value=datetime.fromtimestamp(1, timezone.utc),
                shape=DateShape(
                    min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                    max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
                ),
            )
        self.assertEqual(
            "'default_value' of Parameter must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_parameter_template_level(self):
        parameter = Parameter(
            name="overdraft_fee",
            description="Overdraft fee",
            display_name="Fee charged for balances over the overdraft limit",
            level=ParameterLevel.TEMPLATE,
            default_value=Decimal(15),
            shape=NumberShape(min_value=0, max_value=100, step=Decimal("0.01")),
        )
        self.assertEqual(parameter.default_value, Decimal(15))

    def test_parameter_instance_level(self):
        parameter = Parameter(
            name="minimum_interest_rate",
            description="Minimum interest rate",
            display_name="Minimum interest rate paid on positive balances",
            level=ParameterLevel.INSTANCE,
            update_permission=ParameterUpdatePermission.FIXED,
            derived=False,
            default_value=Decimal(1.0),
            shape=NumberShape(min_value=0, max_value=100, step=Decimal("0.01")),
        )
        self.assertEqual(parameter.default_value, Decimal(1.0))

    def test_parameter_string_shape(self):
        parameter = Parameter(
            name="string_parameter",
            description="template level string parameter",
            display_name="Test Parameter",
            level=ParameterLevel.TEMPLATE,
            shape=StringShape(),
        )
        self.assertTrue(isinstance(parameter.shape, StringShape))

    def test_parameter_account_id_shape(self):
        parameter = Parameter(
            name="account_id",
            description="template level account id parameter",
            display_name="Test Parameter",
            level=ParameterLevel.TEMPLATE,
            shape=AccountIdShape(),
        )
        self.assertTrue(isinstance(parameter.shape, AccountIdShape))

    def test_parameter_denomination_shape(self):
        parameter = Parameter(
            name="denomination",
            description="template level denomination parameter",
            display_name="Test Parameter",
            level=ParameterLevel.TEMPLATE,
            shape=DenominationShape(),
        )
        self.assertTrue(isinstance(parameter.shape, DenominationShape))

    def test_parameter_date_shape(self):
        date_shape = DateShape(
            min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
            max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
        )
        parameter = Parameter(
            name="bonus_date",
            description="Date account bonus will be paid",
            display_name="Bonus date",
            level=ParameterLevel.TEMPLATE,
            shape=date_shape,
        )
        self.assertEqual(parameter.shape, date_shape)

    def test_parameter_date_shape_min_date_raise_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2020, 1, 1),
                max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'min_date' of DateShape is not timezone aware.",
            str(ex.exception),
        )

    def test_parameter_date_shape_min_date_raise_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("US/Pacific")),
                max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'min_date' of DateShape must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_parameter_date_shape_min_date_raise_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime.fromtimestamp(1, timezone.utc),
                max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'min_date' of DateShape must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_parameter_date_shape_max_date_raise_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                max_date=datetime(2020, 3, 31),
            )
        self.assertEqual(
            "'max_date' of DateShape is not timezone aware.",
            str(ex.exception),
        )

    def test_parameter_date_shape_max_date_raise_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                max_date=datetime(2020, 3, 31, tzinfo=ZoneInfo("US/Pacific")),
            )
        self.assertEqual(
            "'max_date' of DateShape must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_parameter_date_shape_max_date_raise_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2020, 1, 1, tzinfo=ZoneInfo("UTC")),
                max_date=datetime.fromtimestamp(1, timezone.utc),
            )
        self.assertEqual(
            "'max_date' of DateShape must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_parameter_not_using_shape_instance(self):
        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                default_value=27,
                derived=False,
                shape=NumberShape,
            )
        self.assertEqual(
            str(ex.exception),
            "Parameter init arg 'shape' for parameter 'day_of_month' must be an instance of the "
            "NumberShape class",
        )

    def test_parameter_invalid_shape(self):
        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                default_value=27,
                derived=False,
                shape=Decimal,
            )
        self.assertEqual(
            str(ex.exception),
            "Parameter attribute 'shape' expected Union[AccountIdShape, DateShape, "
            "DenominationShape, NumberShape, OptionalShape, StringShape, UnionShape], got "
            "'<class 'decimal.Decimal'>'",
        )

    def test_derived_parameters_cannot_have_default_values(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Parameter(
                name="overdraft_limit",
                level=ParameterLevel.INSTANCE,
                description="Overdraft limit",
                shape=StringShape(),
                default_value="1",
                derived=True,
            )
        self.assertEqual(
            "Derived Parameters cannot have a default value or update permissions: "
            "overdraft_limit",
            str(ex.exception),
        )

    def test_parameter_default_value_multiple_optional_value(self):
        with self.assertRaises(StrongTypingError) as ex:
            Parameter(
                name="day_of_month",
                description="Which day would you like interest to be paid?",
                display_name="Day of month to pay interest",
                level=ParameterLevel.GLOBAL,
                derived=False,
                shape=OptionalShape(shape=NumberShape()),
                default_value=OptionalValue(OptionalValue(1)),
            )
        expected = (
            "'OptionalValue.value' expected Union[Decimal, str, datetime, UnionItemValue, int] "
            + "if populated, got 'OptionalValue(value=1)' of type OptionalValue"
        )
        self.assertEqual(expected, str(ex.exception))

    # Shapes

    # NumberShape

    def test_number_shape_init(self):
        with self.assertRaises(StrongTypingError) as ex:
            NumberShape(min_value="")
        self.assertEqual(
            str(ex.exception),
            "'min_value' expected Union[Decimal, int] if populated, got '' " "of type str",
        )

        with self.assertRaises(StrongTypingError) as ex:
            NumberShape(min_value=1, max_value="")
        self.assertEqual(
            str(ex.exception),
            "'max_value' expected Union[Decimal, int] if populated, got '' of type str",
        )

        with self.assertRaises(StrongTypingError) as ex:
            NumberShape(min_value=1, max_value=2, step="")
        self.assertEqual(
            str(ex.exception),
            "'step' expected Union[Decimal, int] if populated, got '' of type str",
        )

        with self.assertRaises(InvalidSmartContractError) as ex:
            NumberShape(min_value=2, max_value=1)
        self.assertEqual(str(ex.exception), "NumberShape min_value must be less than max_value")

        valid_number_shape = NumberShape(min_value=1, max_value=2, step=Decimal(0.01))
        self.assertEqual(valid_number_shape.min_value, 1)
        self.assertEqual(valid_number_shape.max_value, 2)
        self.assertEqual(valid_number_shape.step, Decimal(0.01))

    def test_number_shape_repr(self):
        shape = NumberShape(min_value=1, max_value=5, step=1)
        expected = "NumberShape(min_value=1, max_value=5, step=1)"
        self.assertEqual(expected, repr(shape))

    def test_number_shape_equality(self):
        shape = NumberShape(min_value=1, max_value=2)
        other_shape = NumberShape(min_value=1, max_value=2)

        self.assertEqual(shape, other_shape)

    def test_number_shape_unequal_max_value(self):
        shape = NumberShape(min_value=1, max_value=2)
        other_shape = NumberShape(min_value=1, max_value=42)

        self.assertNotEqual(shape, other_shape)

    # StringShape

    def test_string_shape_repr(self):
        shape = StringShape()
        expected = "StringShape()"
        self.assertEqual(expected, repr(shape))

    def test_string_shape_equality(self):
        shape = StringShape()
        other_shape = StringShape()

        self.assertEqual(shape, other_shape)

    # DateShape

    def test_date_shape_init(self):
        with self.assertRaises(StrongTypingError) as ex:
            DateShape(min_date="")
        self.assertEqual(
            str(ex.exception), "'min_date' expected datetime if populated, got '' of type str"
        )

        with self.assertRaises(StrongTypingError) as ex:
            DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")), max_date="")
        self.assertEqual(
            str(ex.exception), "'max_date' expected datetime if populated, got '' of type str"
        )

        with self.assertRaises(InvalidSmartContractError) as ex:
            DateShape(
                min_date=datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC")),
                max_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(str(ex.exception), "DateShape min_date must be less than max_date")

        valid_date_shape_1 = DateShape()
        valid_date_shape_2 = DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))
        valid_date_shape_3 = DateShape(max_date=datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC")))

        self.assertEqual(valid_date_shape_1.min_date, None)
        self.assertEqual(valid_date_shape_1.max_date, None)
        self.assertEqual(valid_date_shape_2.min_date, datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))
        self.assertEqual(valid_date_shape_2.max_date, None)
        self.assertEqual(valid_date_shape_3.min_date, None)
        self.assertEqual(valid_date_shape_3.max_date, datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC")))

    def test_date_shape_repr(self):
        shape = DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))
        expected = (
            "DateShape(min_date=datetime.datetime(1999, 1, 1, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), max_date=None)"
        )
        self.assertEqual(expected, repr(shape))

    def test_date_shape_equality(self):
        shape = DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))
        other_shape = DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))

        self.assertEqual(shape, other_shape)

    def test_date_shape_unequal_min_date(self):
        shape = DateShape(min_date=datetime(1999, 1, 1, tzinfo=ZoneInfo("UTC")))
        other_shape = DateShape(min_date=datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC")))

        self.assertNotEqual(shape, other_shape)

    # AccountIdShape

    def test_account_id_shape_repr(self):
        shape = AccountIdShape()
        expected = "AccountIdShape()"
        self.assertEqual(expected, repr(shape))

    def test_account_id_shape_equality(self):
        shape = AccountIdShape()
        other_shape = AccountIdShape()

        self.assertEqual(shape, other_shape)

    # DenominationShape

    def test_denomination_shape_repr(self):
        shape = DenominationShape(permitted_denominations=["GBP"])
        expected = "DenominationShape(permitted_denominations=['GBP'])"
        self.assertEqual(expected, repr(shape))

    def test_denomination_shape_equality(self):
        shape = DenominationShape(permitted_denominations=["GBP"])
        other_shape = DenominationShape(permitted_denominations=["GBP"])

        self.assertEqual(shape, other_shape)

    def test_denomination_shape_unequal_max_value(self):
        shape = DenominationShape(permitted_denominations=["GBP"])
        other_shape = DenominationShape(permitted_denominations=["USD"])

        self.assertNotEqual(shape, other_shape)

    # UnionShape

    def test_union_shape_init(self):
        with self.assertRaises(TypeError) as ex:
            UnionShape()
        self.assertEqual(
            str(ex.exception),
            "UnionShape.__init__() missing 1 required keyword-only argument: 'items'",
        )

        with self.assertRaises(StrongTypingError) as ex:
            UnionShape(items=1)
        self.assertEqual(
            str(ex.exception),
            "UnionShape __init__ Expected list of UnionItem objects for " "'items', got '1'",
        )

        with self.assertRaises(InvalidSmartContractError) as ex:
            UnionShape(items=[])
        self.assertEqual(str(ex.exception), "'items' must be a non empty list, got []")

        with self.assertRaises(StrongTypingError) as ex:
            UnionShape(items=[1, 2, 3])
        self.assertEqual(
            str(ex.exception), "UnionShape __init__ Expected UnionItem, got '1' of type int"
        )

        union_item = UnionItem(key="key", display_name="display_name")
        valid_union_shape = UnionShape(items=[union_item])
        self.assertEqual(valid_union_shape.items[0], union_item)

    def test_union_shape_repr(self):
        union_item = UnionItem(key="key", display_name="display_name")
        shape = UnionShape(items=[union_item])
        expected = "UnionShape(items=[UnionItem(key='key', display_name='display_name')])"
        self.assertEqual(expected, repr(shape))

    def test_union_shape_equality(self):
        union_item = UnionItem(key="key", display_name="display_name")
        shape = UnionShape(items=[union_item])

        other_union_item = UnionItem(key="key", display_name="display_name")
        other_shape = UnionShape(items=[other_union_item])

        self.assertEqual(shape, other_shape)

    def test_union_shape_unequal_items(self):
        union_item = UnionItem(key="key", display_name="display_name")
        shape = UnionShape(items=[union_item])

        other_union_item = UnionItem(key="key", display_name="display_eman")
        other_shape = UnionShape(items=[other_union_item])

        self.assertNotEqual(shape, other_shape)

    # UnionItem

    def test_union_item_init(self):
        with self.assertRaises(StrongTypingError) as ex:
            UnionItem(key=None, display_name=None)
        self.assertEqual(str(ex.exception), "UnionItem init arg 'key' must be populated")

        with self.assertRaises(StrongTypingError) as ex:
            UnionItem(key="", display_name=None)
        self.assertEqual(str(ex.exception), "UnionItem init arg 'key' must be populated")

        with self.assertRaises(StrongTypingError) as ex:
            UnionItem(key="KEY", display_name=None)
        self.assertEqual(str(ex.exception), "UnionItem init arg 'display_name' must be populated")

        with self.assertRaises(StrongTypingError) as ex:
            UnionItem(key="KEY", display_name="")
        self.assertEqual(str(ex.exception), "UnionItem init arg 'display_name' must be populated")

        valid_union_item = UnionItem(key="KEY", display_name="display_name")
        self.assertEqual(valid_union_item.key, "KEY")
        self.assertEqual(valid_union_item.display_name, "display_name")

    def test_union_item_repr(self):
        item = UnionItem(key="KEY", display_name="display_name")
        expected = "UnionItem(key='KEY', display_name='display_name')"
        self.assertEqual(expected, repr(item))

    def test_union_item_equality(self):
        item = UnionItem(key="bob", display_name="ken")
        other_item = UnionItem(key="bob", display_name="ken")
        self.assertEqual(item, other_item)

    def test_union_item_unequal_key(self):
        item = UnionItem(key="bob", display_name="ken")
        other_item = UnionItem(key="alice", display_name="ken")
        self.assertNotEqual(item, other_item)

    # UnionItemValue

    def test_union_item_value_repr(self):
        value = UnionItemValue(key="KEY")
        expected = "UnionItemValue(key='KEY')"
        self.assertEqual(expected, repr(value))

    def test_union_item_value_equality(self):
        value = UnionItemValue(key="bob")
        other_value = UnionItemValue(key="bob")
        self.assertEqual(value, other_value)

    def test_union_item_value_unequal_key(self):
        value = UnionItemValue(key="bob")
        other_value = UnionItemValue(key="alice")
        self.assertNotEqual(value, other_value)

    # OptionalShape

    def test_optional_shape_init(self):
        with self.assertRaises(TypeError) as ex:
            OptionalShape()
        self.assertEqual(
            str(ex.exception),
            "OptionalShape.__init__() missing 1 required keyword-only argument: 'shape'",
        )

        with self.assertRaises(TypeError) as ex:
            OptionalShape(1)
        self.assertEqual(
            str(ex.exception),
            "OptionalShape.__init__() takes 1 positional argument but 2 were given",
        )

        with self.assertRaises(StrongTypingError) as ex:
            OptionalShape(shape=1)
        self.assertEqual(
            str(ex.exception),
            "'shape' expected Union[AccountIdShape, DateShape, DenominationShape, NumberShape, "
            "StringShape, UnionShape], got '1' of type int",
        )

        with self.assertRaises(StrongTypingError) as ex:
            OptionalShape(shape=StringShape)
        self.assertEqual(
            str(ex.exception),
            "OptionalShape init arg 'shape' must be an instance of StringShape class",
        )

        shape = StringShape()
        valid_optional_shape = OptionalShape(shape=shape)
        self.assertEqual(valid_optional_shape.shape, shape)

    def test_optional_shape_repr(self):
        optional_value = OptionalShape(
            shape=NumberShape(min_value=1, max_value=2, step=Decimal("0.01"))
        )
        expected = (
            "OptionalShape(shape=NumberShape(min_value=1, max_value=2, step=Decimal('0.01')))"
        )
        self.assertEqual(expected, repr(optional_value))

    def test_optional_shape_equality(self):
        optional_value = OptionalShape(
            shape=NumberShape(min_value=1, max_value=2, step=Decimal(0.01))
        )
        other_optional_value = OptionalShape(
            shape=NumberShape(min_value=1, max_value=2, step=Decimal(0.01))
        )

        self.assertEqual(optional_value, other_optional_value)

    def test_optional_shape_unequal_shape(self):
        optional_value = OptionalShape(
            shape=NumberShape(min_value=1, max_value=2, step=Decimal(0.01))
        )
        other_optional_value = OptionalShape(
            shape=NumberShape(min_value=1, max_value=42, step=Decimal(0.01))
        )

        self.assertNotEqual(optional_value, other_optional_value)

    # OptionalValue

    def test_optional_value_init(self):
        with self.assertRaises(StrongTypingError) as ex:
            OptionalValue(AccountIdShape())
        expected = (
            "'OptionalValue.value' expected Union[Decimal, str, datetime, UnionItemValue, int] "
            + "if populated, got 'AccountIdShape()' of type AccountIdShape"
        )
        self.assertEqual(str(ex.exception), expected)

        with self.assertRaises(StrongTypingError) as ex:
            OptionalValue([])
        self.assertEqual(
            str(ex.exception),
            "'OptionalValue.value' expected Union[Decimal, str, datetime, UnionItemValue, int] "
            + "if populated, got '[]' of type list",
        )

        self.assertEqual(OptionalValue("").value, "")

        valid_optional_value = OptionalValue(1)
        self.assertEqual(valid_optional_value.value, 1)
        self.assertEqual(valid_optional_value.is_set(), True)
        valid_optional_value.value = None
        self.assertEqual(valid_optional_value.is_set(), False)

    def test_optional_value_repr(self):
        value = OptionalValue(45)
        expected = "OptionalValue(value=45)"
        self.assertEqual(expected, repr(value))

    def test_optional_value_equality(self):
        optional_value = OptionalValue(1)
        other_optional_value = OptionalValue(1)
        self.assertEqual(optional_value, other_optional_value)

    def test_optional_value_unequal_value(self):
        optional_value = OptionalValue(1)
        other_optional_value = OptionalValue(42)
        self.assertNotEqual(optional_value, other_optional_value)

    # Enums

    def test_posting_instruction_type_enum(self):
        self.assertEqual(PostingInstructionType.AUTHORISATION.value, "Authorisation")
        self.assertEqual(
            PostingInstructionType.AUTHORISATION_ADJUSTMENT.value,
            "AuthorisationAdjustment",
        )
        self.assertEqual(PostingInstructionType.CUSTOM_INSTRUCTION.value, "CustomInstruction")
        self.assertEqual(PostingInstructionType.HARD_SETTLEMENT.value, "HardSettlement")
        self.assertEqual(PostingInstructionType.RELEASE.value, "Release")
        self.assertEqual(PostingInstructionType.SETTLEMENT.value, "Settlement")
        self.assertEqual(PostingInstructionType.TRANSFER.value, "Transfer")

    def test_phase_enum(self):
        self.assertEqual(Phase.PENDING_IN.value, "pending_in")
        self.assertEqual(Phase.PENDING_OUT.value, "pending_out")
        self.assertEqual(Phase.COMMITTED.value, "committed")

    def test_tside_enum(self):
        self.assertEqual(Tside.ASSET.value, 1)
        self.assertEqual(Tside.LIABILITY.value, 2)

    def test_level_enum(self):
        self.assertEqual(ParameterLevel.GLOBAL.value, 1)
        self.assertEqual(ParameterLevel.TEMPLATE.value, 2)
        self.assertEqual(ParameterLevel.INSTANCE.value, 3)

    def test_rejection_reason_enum(self):
        self.assertEqual(RejectionReason.UNKNOWN_REASON.value, 0)
        self.assertEqual(RejectionReason.INSUFFICIENT_FUNDS.value, 1)
        self.assertEqual(RejectionReason.WRONG_DENOMINATION.value, 2)
        self.assertEqual(RejectionReason.AGAINST_TNC.value, 3)
        self.assertEqual(RejectionReason.CLIENT_CUSTOM_REASON.value, 4)

    def test_update_permission_enum(self):
        self.assertEqual(ParameterUpdatePermission.PERMISSION_UNKNOWN.value, 0)
        self.assertEqual(ParameterUpdatePermission.FIXED.value, 1)
        self.assertEqual(ParameterUpdatePermission.OPS_EDITABLE.value, 2)
        self.assertEqual(ParameterUpdatePermission.USER_EDITABLE.value, 3)
        self.assertEqual(ParameterUpdatePermission.USER_EDITABLE_WITH_OPS_PERMISSION.value, 4)

    def test_supervision_execution_mode_enum(self):
        self.assertEqual(SupervisionExecutionMode.OVERRIDE.value, 1)
        self.assertEqual(SupervisionExecutionMode.INVOKED.value, 2)

    def test_timeline_enum(self):
        self.assertEqual(Timeline.PRESENT.value, 1)
        self.assertEqual(Timeline.FUTURE.value, 2)

    

    # SupervisorActivationHookResult

    def test_supervisor_activation_hook_result(self):
        supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=self.test_scheduled_events_return_value
        )
        self.assertEqual(
            self.test_scheduled_events_return_value,
            supervisor_activation_hook_result.scheduled_events_return_value,
        )
        self.assertIsNone(supervisor_activation_hook_result.rejection)

    def test_supervisor_activation_hook_result_repr(self):
        supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=self.test_scheduled_events_return_value
        )
        expected = (
            "SupervisorActivationHookResult(scheduled_events_return_value={'event_1': "
            + "ScheduledEvent(start_datetime=datetime.datetime(1970, 1, 1, 0, 0, 1, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "end_datetime=datetime.datetime(1970, 1, 1, 0, 0, 2, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), expression=ScheduleExpression(day='1', "
            + "day_of_week=None, hour='0', minute='0', second='0', month='1', year='2000'), "
            + "schedule_method=None, skip=ScheduleSkip(end=datetime.datetime(1970, 1, 1, 0, 0, 3, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')))), 'event_2': "
            + "ScheduledEvent(start_datetime=datetime.datetime(1970, 1, 1, 0, 0, 5, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "end_datetime=datetime.datetime(1970, 1, 1, 0, 0, 6, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), expression="
            + "ScheduleExpression(day=None, day_of_week='mon', hour=None, minute=None, "
            + "second=None, month=None, year=None), schedule_method=None, skip=False)}, "
            + "rejection=None)"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(supervisor_activation_hook_result))

    def test_supervisor_activation_hook_result_equality(self):
        supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=self.test_scheduled_events_return_value
        )
        other_scheduled_events_return_value = {
            "event_1": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(1970, 1, 1, second=2, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(
                    year="2000",
                    month="1",
                    day="1",
                    hour="0",
                    minute="0",
                    second="0",
                ),
                skip=ScheduleSkip(
                    end=datetime(1970, 1, 1, second=3, tzinfo=ZoneInfo("UTC")),
                ),
            ),
            "event_2": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=5, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(1970, 1, 1, second=6, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(
                    day_of_week="mon",
                ),
            ),
        }
        other_supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=other_scheduled_events_return_value
        )

        self.assertEqual(
            supervisor_activation_hook_result,
            other_supervisor_activation_hook_result,
        )

    def test_supervisor_activation_hook_result_unequal_scheduled_events_return_value(self):
        supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=self.test_scheduled_events_return_value
        )
        other_scheduled_events_return_value = {
            "event_1": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(1970, 1, 1, second=2, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(
                    year="2000",
                    month="1",
                    day="1",
                    hour="0",
                    minute="0",
                    second="0",
                ),
                skip=ScheduleSkip(
                    end=datetime(1970, 1, 1, second=5, tzinfo=ZoneInfo("UTC")),
                ),
            ),
            "event_2": ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=5, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(1970, 1, 1, second=6, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(
                    day_of_week="mon",
                ),
            ),
        }
        other_supervisor_activation_hook_result = SupervisorActivationHookResult(
            scheduled_events_return_value=other_scheduled_events_return_value
        )

        self.assertNotEqual(
            supervisor_activation_hook_result,
            other_supervisor_activation_hook_result,
        )

    

    def test_supervisor_activation_hook_result_no_events(self):
        supervisor_activation_hook_result = SupervisorActivationHookResult()
        self.assertEqual({}, supervisor_activation_hook_result.scheduled_events_return_value)
        

    # SupervisorConversionHookResult

    def test_supervisor_conversion_hook_result(self):
        supervisor_conversion_hook_result = SupervisorConversionHookResult(
            scheduled_events_return_value=self.test_scheduled_events_return_value
        )
        self.assertEqual(
            self.test_scheduled_events_return_value,
            supervisor_conversion_hook_result.scheduled_events_return_value,
        )
        

    def test_supervisor_conversion_hook_result_no_events(self):
        supervisor_conversion_hook_result = SupervisorConversionHookResult()
        self.assertEqual({}, supervisor_conversion_hook_result.scheduled_events_return_value)
        

    

    # FlagsFilter

    def test_flags_filter_repr(self):
        flags_filter = FlagsFilter(
            flag_definition_ids=["flag_definition_id_1", "flag_definition_id_2"]
        )
        expected = (
            "FlagsFilter(flag_definition_ids=['flag_definition_id_1', 'flag_definition_id_2'])"
        )
        self.assertEqual(expected, repr(flags_filter))

    def test_flags_filter_attributes(self):
        flag_definition_ids = ["flag_definition_id_1", "flag_definition_id_2"]
        flags_filter = FlagsFilter(flag_definition_ids=flag_definition_ids)
        self.assertEqual(flag_definition_ids, flags_filter.flag_definition_ids)

    def test_flags_filter_equality(self):
        flag_definition_ids = ["flag_definition_id_1", "flag_definition_id_2"]
        flags_filter_1 = FlagsFilter(flag_definition_ids=flag_definition_ids)
        flags_filter_2 = FlagsFilter(flag_definition_ids=flag_definition_ids)
        self.assertEqual(flags_filter_1, flags_filter_2)

    def test_flags_filter_unequal_flag_definition_ids(self):
        flags_filter_1 = FlagsFilter(
            flag_definition_ids=["flag_definition_id_1", "flag_definition_id_2"]
        )
        flags_filter_2 = FlagsFilter(flag_definition_ids=["flag_definition_id_1"])
        self.assertNotEqual(flags_filter_1, flags_filter_2)

    def test_flags_filter_raises_with_empty_flag_definition_ids(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsFilter(flag_definition_ids=[])
        self.assertEqual(
            str(e.exception), "'FlagsFilter.flag_definition_ids' must be a non empty list, got []"
        )

    def test_flags_filter_raises_with_empty_flag_definition_ids_field(self):
        with self.assertRaises(TypeError) as e:
            FlagsFilter()
        self.assertEqual(
            str(e.exception),
            "FlagsFilter.__init__() missing 1 "
            "required keyword-only argument: 'flag_definition_ids'",
        )

    def test_flags_filter_raises_with_flag_definition_ids_invalid_element_type_nested(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsFilter(flag_definition_ids=["string", 1, 2])
        self.assertEqual(
            str(e.exception), "'FlagsFilter.flag_definition_ids' expected str, got '1' of type int"
        )

    def test_flags_filter_raises_with_flag_definition_ids_invalid_element_type_not_nested(self):
        with self.assertRaises(StrongTypingError) as e:
            FlagsFilter(flag_definition_ids=3.14159265359)
        self.assertEqual(
            str(e.exception),
            "'FlagsFilter.flag_definition_ids' expected List[str], got "
            "'3.14159265359' of type float",
        )

    def test_flags_filter_raises_with_duplicate_flag_definition_ids(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsFilter(flag_definition_ids=["flag_definition_id_1", "flag_definition_id_1"])
        self.assertEqual(
            str(e.exception),
            "FlagsFilter flag_definition_ids must not contain any duplicate flag definition ids.",
        )

    # FlagsObservation

    def test_flags_observation(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation = FlagsObservation(
            flags=deepcopy(flags), value_datetime=deepcopy(value_datetime)
        )
        self.assertEqual(value_datetime, flags_observation.value_datetime)
        self.assertEqual(flags, flags_observation.flags)

    def test_flags_observation_no_value_datetime(self):
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation = FlagsObservation(flags=deepcopy(flags))
        self.assertIsNone(flags_observation.value_datetime)
        self.assertEqual(flags, flags_observation.flags)

    def test_flags_observation_equality(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation_1 = FlagsObservation(flags=flags, value_datetime=value_datetime)
        flags_observation_2 = FlagsObservation(
            flags=deepcopy(flags), value_datetime=deepcopy(value_datetime)
        )
        self.assertEqual(flags_observation_1, flags_observation_2)

    def test_flags_observation_equality_different_from_proto(self):
        """Should be equal if all public attributes are equal by value."""
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation_1 = FlagsObservation(flags=flags, value_datetime=value_datetime)
        flags_observation_2 = FlagsObservation(
            flags=deepcopy(flags), value_datetime=deepcopy(value_datetime), _from_proto=True
        )
        self.assertEqual(flags_observation_1, flags_observation_2)

    def test_flags_observation_unequal_flags(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        flags_1 = {"flag_def_1": True, "flag_def_2": False}
        flags_2 = {"flag_def_1": False, "flag_def_2": False}
        flags_observation_1 = FlagsObservation(flags=flags_1, value_datetime=value_datetime)
        flags_observation_2 = FlagsObservation(flags=flags_2, value_datetime=value_datetime)
        self.assertNotEqual(flags_observation_1, flags_observation_2)

    def test_flags_observation_unequal_datetime(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        christmas_day = datetime(year=2022, month=12, day=25, tzinfo=ZoneInfo("UTC"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation_1 = FlagsObservation(flags=flags, value_datetime=value_datetime)
        flags_observation_2 = FlagsObservation(flags=flags, value_datetime=christmas_day)
        self.assertNotEqual(flags_observation_1, flags_observation_2)

    def test_flags_observation_repr(self):
        christmas_day = datetime(year=2022, month=12, day=25, tzinfo=ZoneInfo("UTC"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        flags_observation = FlagsObservation(flags=flags, value_datetime=christmas_day)
        expected_repr = (
            "FlagsObservation(value_datetime=datetime.datetime(2022, 12, 25, 0, 0, "
            "tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            "flags={'flag_def_1': True, 'flag_def_2': False})"
        )
        self.assertEqual(expected_repr, repr(flags_observation))

    def test_flags_observation_repr_empty_flags(self):
        flags_observation = FlagsObservation(flags=defaultdict(lambda: False), value_datetime=None)
        expected_repr = "FlagsObservation(value_datetime=None, flags={})"
        self.assertEqual(expected_repr, repr(flags_observation))

    def test_flags_observation_raises_error_with_wrong_flags_type(self):
        with self.assertRaises(StrongTypingError) as e:
            christmas_day = datetime(year=2022, month=12, day=25, tzinfo=ZoneInfo("UTC"))
            FlagsObservation(flags=1, value_datetime=christmas_day)
        self.assertEqual(
            "'FlagsObservation.flags' expected dict[str, bool], got '1' of type int",
            str(e.exception),
        )

    def test_flags_observation_raises_error_with_wrong_value_datetime_type(self):
        with self.assertRaises(StrongTypingError) as e:
            flags = {"flag_def_1": True, "flag_def_2": False}
            FlagsObservation(flags=flags, value_datetime=1)
        self.assertEqual(
            "'FlagsObservation.value_datetime' expected datetime if populated, got '1' of type int",
            str(e.exception),
        )

    def test_flags_observation_raises_error_with_value_datetime_not_timezone_aware(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            naive_datetime = datetime(year=2020, month=2, day=20)
            flags = {"flag_def_1": True, "flag_def_2": False}
            FlagsObservation(flags=flags, value_datetime=naive_datetime)
        self.assertEqual(
            "'value_datetime' of FlagsObservation is not timezone aware.", str(e.exception)
        )

    def test_flags_observation_raises_with_non_utc_timezone(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("US/Pacific"))
        flags = {"flag_def_1": True, "flag_def_2": False}
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsObservation(flags=flags, value_datetime=value_datetime)
        self.assertEqual(
            str(e.exception),
            "'value_datetime' of FlagsObservation must have timezone UTC, currently " "US/Pacific.",
        )

    def test_flags_observation_raises_with_non_zoneinfo_timezone(self):
        value_datetime = datetime.fromtimestamp(1, timezone.utc)
        flags = {"flag_def_1": True, "flag_def_2": False}
        with self.assertRaises(InvalidSmartContractError) as e:
            FlagsObservation(flags=flags, value_datetime=value_datetime)
        self.assertEqual(
            "'value_datetime' of FlagsObservation must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(e.exception),
        )

    def test_flags_observation_no_value_datetime_and_empty_balances(self):
        flags = {}
        flags_observation = FlagsObservation(flags=flags)
        self.assertIsNone(flags_observation.value_datetime)
        self.assertEqual({}, flags_observation.flags)

    # ScheduleExpression

    def test_schedule_expression_can_be_created(self):
        schedule_expression = ScheduleExpression(day="day", year="year")
        self.assertEqual(schedule_expression.day, "day")
        self.assertEqual(schedule_expression.year, "year")

    def test_schedule_expression_equality(self):
        schedule_expression = ScheduleExpression(day="day", year="year")
        other_schedule_expression = ScheduleExpression(day="day", year="year")
        self.assertEqual(schedule_expression, other_schedule_expression)

    def test_schedule_expression_unequal_year(self):
        schedule_expression = ScheduleExpression(day="day", year="year")
        other_schedule_expression = ScheduleExpression(day="day", year="year2")
        self.assertNotEqual(schedule_expression, other_schedule_expression)

    def test_schedule_expression_repr(self):
        schedule_expression = ScheduleExpression(
            day=15,
            day_of_week=3,
            hour=30,
            minute=30,
            second=30,
            month=6,
            year=2000,
        )
        expected = (
            "ScheduleExpression(day=15, day_of_week=3, "
            + "hour=30, minute=30, second=30, month=6, year=2000)"
        )
        self.assertEqual(expected, repr(schedule_expression))

    def test_schedule_expression_int_values(self):
        schedule_expression = ScheduleExpression(
            day=15,
            day_of_week=3,
            hour=30,
            minute=30,
            second=30,
            month=6,
            year=2000,
        )
        self.assertEqual(schedule_expression.day, 15)
        self.assertEqual(schedule_expression.day_of_week, 3)
        self.assertEqual(schedule_expression.hour, 30)
        self.assertEqual(schedule_expression.minute, 30)
        self.assertEqual(schedule_expression.second, 30)
        self.assertEqual(schedule_expression.month, 6)
        self.assertEqual(schedule_expression.year, 2000)

    def test_schedule_expression_zero_values(self):
        schedule_expression = ScheduleExpression(
            hour=0,
        )
        self.assertEqual(schedule_expression.hour, 0)
        # Defaults
        self.assertIsNone(schedule_expression.day)
        self.assertIsNone(schedule_expression.day_of_week)
        self.assertIsNone(schedule_expression.minute)
        self.assertIsNone(schedule_expression.second)
        self.assertIsNone(schedule_expression.month)
        self.assertIsNone(schedule_expression.year)

    def test_schedule_expression_string_values(self):
        schedule_expression = ScheduleExpression(
            day="*/2",
            day_of_week="MON",
            hour="1,2,3",
            minute="*/15",
            second="*/30",
            month="*",
            year="*",
        )
        self.assertEqual(schedule_expression.day, "*/2")
        self.assertEqual(schedule_expression.day_of_week, "MON")
        self.assertEqual(schedule_expression.hour, "1,2,3")
        self.assertEqual(schedule_expression.minute, "*/15")
        self.assertEqual(schedule_expression.second, "*/30")
        self.assertEqual(schedule_expression.month, "*")
        self.assertEqual(schedule_expression.year, "*")

    def test_schedule_expression_invalid_type_day(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                day=False,
                year=2000,
            )
        expected = "'day' expected Union[int, str] if populated, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_day_of_week(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                day_of_week=False,
                month=6,
            )
        expected = "'day_of_week' expected Union[int, str] if populated, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_hour(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                day=15,
                hour=(),
            )
        expected = "'hour' expected Union[int, str] if populated, got '()' of type tuple"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_minute(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                hour=30,
                minute={},
            )
        expected = "'minute' expected Union[int, str] if populated, got '{}' of type dict"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_second(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                second=False,
            )
        expected = "'second' expected Union[int, str] if populated, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_month(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                month=False,
                year=2000,
            )
        expected = "'month' expected Union[int, str] if populated, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_schedule_expression_invalid_type_year(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleExpression(
                year=False,
            )
        expected = "'year' expected Union[int, str] if populated, got 'False' of type bool"
        self.assertEqual(expected, str(ex.exception))

    def test_empty_schedule_expression_raises(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduleExpression()
        expected = "Empty ScheduleExpression not allowed"
        self.assertEqual(expected, str(ex.exception))

    # EventTypesGroup

    def test_event_types_group_can_be_created(self):
        event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"]
        )
        self.assertEqual(event_types_group.name, "TestEventTypesGroup")
        self.assertEqual(event_types_group.event_types_order, ["EVENT_TYPE1", "EVENT_TYPE2"])

    def test_event_types_group_equality(self):
        event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"]
        )
        other_event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"]
        )

        self.assertEqual(event_types_group, other_event_types_group)

    def test_event_types_group_unequal_event_types_order(self):
        event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"]
        )
        other_event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE3"]
        )

        self.assertNotEqual(event_types_group, other_event_types_group)

    def test_event_types_group_repr(self):
        event_types_group = EventTypesGroup(
            name="TestEventTypesGroup", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"]
        )
        expected = (
            "EventTypesGroup(name='TestEventTypesGroup', "
            + "event_types_order=['EVENT_TYPE1', 'EVENT_TYPE2'])"
        )
        self.assertEqual(expected, repr(event_types_group))

    def test_event_types_group_empty_name(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            EventTypesGroup(name="", event_types_order=["EVENT_TYPE1", "EVENT_TYPE2"])
        self.assertEqual("EventTypesGroup 'name' must be populated", str(ex.exception))

    def test_event_types_group_raises_with_empty_event_types_order(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            EventTypesGroup(name="TestEvenTypesGroup", event_types_order=[])
        self.assertEqual("'event_types_order' must be a non empty list, got []", str(ex.exception))

    def test_event_types_group_not_enough_event_types(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            EventTypesGroup(name="TestEvenTypesGroup", event_types_order=["EVENT_TYPE"])
        self.assertEqual("An EventTypesGroup must have at least two event types", str(ex.exception))

    # CalendarEvent

    def test_calendar_event(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        self.assertEqual("test 1", calendar_event.id)

    def test_calendar_event_equality(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        other_calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        self.assertEqual(calendar_event, other_calendar_event)

    def test_calendar_event_unequal_start_datetime(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        other_calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(999, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        self.assertNotEqual(calendar_event, other_calendar_event)

    def test_calendar_event_repr(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        expected = (
            "CalendarEvent(id='test 1', calendar_id='123', "
            + "start_datetime=datetime.datetime(2015, 1, 1, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "end_datetime=datetime.datetime(2015, 1, 2, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(calendar_event))

    def test_calendar_event_start_datetime_raises_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime(2015, 1, 1),
                end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'start_datetime' of CalendarEvent is not timezone aware.",
            str(ex.exception),
        )

    def test_calendar_event_start_datetime_raises_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("US/Pacific")),
                end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'start_datetime' of CalendarEvent must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_calendar_event_start_datetime_raises_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime.fromtimestamp(1, timezone.utc),
                end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "'start_datetime' of CalendarEvent must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_calendar_event_end_datetime_raises_with_naive_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(2015, 1, 2),
            )
        self.assertEqual(
            "'end_datetime' of CalendarEvent is not timezone aware.",
            str(ex.exception),
        )

    def test_calendar_event_end_datetime_raises_with_non_utc_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("US/Pacific")),
            )
        self.assertEqual(
            "'end_datetime' of CalendarEvent must have timezone UTC, currently US/Pacific.",
            str(ex.exception),
        )

    def test_calendar_event_end_datetime_raises_with_non_zoneinfo_timezone(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            CalendarEvent(
                id="test 1",
                calendar_id="123",
                start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime.fromtimestamp(1, timezone.utc),
            )
        self.assertEqual(
            "'end_datetime' of CalendarEvent must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(ex.exception),
        )

    def test_calendar_events(self):
        calendar_events = CalendarEvents(
            calendar_events=[
                CalendarEvent(
                    id="test 1",
                    calendar_id="123",
                    start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
                    end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
                ),
                CalendarEvent(
                    id="test 2",
                    calendar_id="124",
                    start_datetime=datetime(2016, 1, 1, tzinfo=ZoneInfo("UTC")),
                    end_datetime=datetime(2016, 1, 2, tzinfo=ZoneInfo("UTC")),
                ),
            ]
        )
        self.assertEqual(2, len(calendar_events))
        self.assertEqual("test 1", calendar_events[0].id)
        self.assertEqual("test 2", calendar_events[1].id)

    # CalendarEvents

    def test_calendar_events_equality(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        other_calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        calendar_events = CalendarEvents(calendar_events=[calendar_event])
        other_calendar_events = CalendarEvents(calendar_events=[other_calendar_event])

        self.assertEqual(calendar_events, other_calendar_events)

    def test_calendar_events_unequal_calendar_events(self):
        calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(2015, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        other_calendar_event = CalendarEvent(
            id="test 1",
            calendar_id="123",
            start_datetime=datetime(2015, 1, 1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(999, 1, 2, tzinfo=ZoneInfo("UTC")),
        )
        calendar_events = CalendarEvents(calendar_events=[calendar_event])
        other_calendar_events = CalendarEvents(calendar_events=[other_calendar_event])

        self.assertNotEqual(calendar_events, other_calendar_events)

    # ScheduleSkip

    def test_schedule_skip_with_end_datetime(self):
        skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )
        self.assertEqual(
            skip_schedule.end, datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )

    def test_schedule_skip_equality(self):
        skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )
        other_skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )

        self.assertEqual(skip_schedule, other_skip_schedule)

    def test_schedule_skip_unequal_end(self):
        skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )
        other_skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("America/Los_Angeles"))
        )

        self.assertNotEqual(skip_schedule, other_skip_schedule)

    def test_schedule_skip_repr(self):
        skip_schedule = ScheduleSkip(
            end=datetime(year=2021, month=12, day=31, tzinfo=ZoneInfo("UTC"))
        )
        expected = (
            "ScheduleSkip(end=datetime.datetime(2021, 12, 31, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(skip_schedule))

    def test_schedule_skip_raises_with_end_datetime_not_provided(self):
        with self.assertRaises(TypeError) as ex:
            ScheduleSkip()
        self.assertEqual(
            "ScheduleSkip.__init__() missing 1 required keyword-only argument: 'end'",
            str(ex.exception),
        )

    def test_schedule_skip_raises_with_end_datetime_none(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduleSkip(end=None)
        self.assertEqual("ScheduleSkip 'end' must be populated", str(ex.exception))

    def test_schedule_skip_raises_with_end_datetime_invalid(self):
        with self.assertRaises(StrongTypingError) as ex:
            ScheduleSkip(end=False)
        self.assertEqual("Expected datetime, got 'False' of type bool", str(ex.exception))

    # Balance

    def test_balance_equality(self):
        balance = Balance(credit=Decimal(42))
        other_balance = Balance(credit=Decimal(42))
        self.assertEqual(balance, other_balance)

    def test_balance_unequal_credit(self):
        balance = Balance(credit=Decimal(42))
        other_balance = Balance(credit=Decimal(11))
        self.assertNotEqual(balance, other_balance)

    def test_balance_repr(self):
        balance = Balance(credit=Decimal(40), debit=Decimal(10), net=-Decimal(30))
        expected = "Balance(credit=Decimal('40'), debit=Decimal('10'), net=Decimal('-30'))"
        self.assertEqual(expected, repr(balance))

    def test_balance_aggregation_add(self):
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=-Decimal(10))
        aggregated_balance = balance_1 + balance_2
        self.assertEqual(30, aggregated_balance.credit)
        self.assertEqual(40, aggregated_balance.debit)
        self.assertEqual(-10, aggregated_balance.net)

    def test_balance_aggregation_iadd(self):
        aggregated_balance = Balance()
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=-Decimal(10))
        aggregated_balance += balance_1
        aggregated_balance += balance_2
        self.assertEqual(30, aggregated_balance.credit)
        self.assertEqual(40, aggregated_balance.debit)
        self.assertEqual(-10, aggregated_balance.net)

    def test_balance_dict_aggregation_add(self):
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=-Decimal(10))
        address = "DEFAULT"
        asset = "COMMERCIAL_BANK_MONEY"
        denomination = "GBP"
        balance_key_committed = BalanceCoordinate(
            account_address=address,
            asset=asset,
            denomination=denomination,
            phase=Phase.COMMITTED,
        )
        balance_key_out = BalanceCoordinate(
            account_address=address,
            asset=asset,
            denomination=denomination,
            phase=Phase.PENDING_OUT,
        )
        balance_key_in = BalanceCoordinate(
            account_address=address,
            asset=asset,
            denomination=denomination,
            phase=Phase.PENDING_IN,
        )

        balance_default_dict_1 = BalanceDefaultDict()
        balance_default_dict_1[balance_key_committed] = balance_1
        balance_default_dict_1[balance_key_out] = balance_1

        balance_default_dict_2 = BalanceDefaultDict()
        balance_default_dict_2[balance_key_out] = balance_2
        balance_default_dict_2[balance_key_in] = balance_2

        aggregated_balance_default_dict = balance_default_dict_1 + balance_default_dict_2

        expected_aggregated_balance_default_dict = BalanceDefaultDict()
        expected_aggregated_balance_default_dict[balance_key_committed] = balance_1
        expected_aggregated_balance_default_dict[balance_key_out] = balance_1
        expected_aggregated_balance_default_dict[balance_key_out] = balance_1 + balance_2
        expected_aggregated_balance_default_dict[balance_key_in] = balance_2

        self.assertEqual(
            expected_aggregated_balance_default_dict[balance_key_committed].net,
            aggregated_balance_default_dict[balance_key_committed].net,
        )

        self.assertEqual(
            expected_aggregated_balance_default_dict[balance_key_out].net,
            aggregated_balance_default_dict[balance_key_out].net,
        )

        self.assertEqual(
            expected_aggregated_balance_default_dict[balance_key_in].net,
            aggregated_balance_default_dict[balance_key_in].net,
        )

    def test_balance_dict_aggregation_iadd(self):
        aggregated_balance_default_dict = BalanceDefaultDict(lambda *_: Balance())
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=-Decimal(10))
        address = "DEFAULT"
        asset = "COMMERCIAL_BANK_MONEY"
        denomination = "GBP"
        balance_key_committed = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.COMMITTED
        )
        balance_key_out = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_OUT
        )
        balance_key_in = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_IN
        )

        balance_default_dict_1 = BalanceDefaultDict()
        balance_default_dict_1[balance_key_committed] = balance_1
        balance_default_dict_1[balance_key_out] = balance_1

        balance_default_dict_2 = BalanceDefaultDict()
        balance_default_dict_2[balance_key_out] = balance_2
        balance_default_dict_2[balance_key_in] = balance_2

        aggregated_balance_default_dict += balance_default_dict_1
        aggregated_balance_default_dict += balance_default_dict_2

        expected_aggregated_balance_default_dict = BalanceDefaultDict()
        expected_aggregated_balance_default_dict[balance_key_committed] = balance_1
        expected_aggregated_balance_default_dict[balance_key_out] = balance_1 + balance_2
        expected_aggregated_balance_default_dict[balance_key_in] = balance_2

        self.assertDictEqual(
            expected_aggregated_balance_default_dict, aggregated_balance_default_dict
        )

    def test_balance_aggregation_radd(self):
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_3 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        aggregated_balance = sum([balance_1, balance_2, balance_3], Balance())
        self.assertEqual(
            Balance(credit=Decimal(60), debit=Decimal(60), net=Decimal(0)), aggregated_balance
        )

    def test_balance_dict_aggregation_radd(self):
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=-Decimal(10))
        address = "DEFAULT"
        asset = "COMMERCIAL_BANK_MONEY"
        denomination = "GBP"
        balance_key_committed = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.COMMITTED
        )
        balance_key_out = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_OUT
        )
        balance_key_in = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_IN
        )

        balance_default_dict_1 = BalanceDefaultDict()
        balance_default_dict_1[balance_key_committed] = balance_1
        balance_default_dict_1[balance_key_out] = balance_1

        balance_default_dict_2 = BalanceDefaultDict()
        balance_default_dict_2[balance_key_out] = balance_2
        balance_default_dict_2[balance_key_in] = balance_2

        aggregated_balance_default_dict = sum(
            [balance_default_dict_1, balance_default_dict_2],
            BalanceDefaultDict(lambda *_: Balance()),
        )

        expected_aggregated_balance_default_dict = BalanceDefaultDict()
        expected_aggregated_balance_default_dict[balance_key_committed] = balance_1
        expected_aggregated_balance_default_dict[balance_key_out] = balance_1 + balance_2
        expected_aggregated_balance_default_dict[balance_key_in] = balance_2

        self.assertDictEqual(
            expected_aggregated_balance_default_dict, aggregated_balance_default_dict
        )

    def test_balance_dict_repr(self):
        balance_1 = Balance(credit=Decimal(20), debit=Decimal(20), net=Decimal(0))
        balance_2 = Balance(credit=Decimal(10), debit=Decimal(20), net=Decimal(-10))
        address = "DEFAULT"
        asset = "COMMERCIAL_BANK_MONEY"
        denomination = "GBP"
        balance_key_committed = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.COMMITTED
        )
        balance_key_out = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_OUT
        )
        balance_key_in = BalanceCoordinate(
            account_address=address, asset=asset, denomination=denomination, phase=Phase.PENDING_IN
        )

        balance_dict = BalanceDefaultDict()
        balance_dict[balance_key_committed] = balance_1
        balance_dict[balance_key_out] = balance_1 + balance_2
        balance_dict[balance_key_in] = balance_2

        expected_balance_dict = (
            "{'BalanceCoordinate(account_address=DEFAULT, asset=COMMERCIAL_BANK_MONEY, "
            "denomination=GBP, phase=Phase.COMMITTED)': 'Balance(credit=20, debit=20, net=0)', "
            "'BalanceCoordinate(account_address=DEFAULT, asset=COMMERCIAL_BANK_MONEY, "
            "denomination=GBP, phase=Phase.PENDING_OUT)': 'Balance(credit=30, debit=40, net=-10)', "
            "'BalanceCoordinate(account_address=DEFAULT, asset=COMMERCIAL_BANK_MONEY, "
            "denomination=GBP, phase=Phase.PENDING_IN)': 'Balance(credit=10, debit=20, net=-10)'}"
        )
        self.assertEqual(repr(balance_dict), expected_balance_dict)

    def test_balance_credit(self):
        balance = Balance(credit=Decimal(100))
        self.assertEqual(balance.credit, Decimal(100))
        self.assertEqual(balance.net, 0)
        self.assertEqual(balance.debit, 0)

    def test_balance_net(self):
        balance = Balance(net=Decimal(120))
        self.assertEqual(balance.credit, 0)
        self.assertEqual(balance.net, Decimal(120))
        self.assertEqual(balance.debit, 0)

    def test_balance_debit(self):
        balance = Balance(debit=Decimal(19.99))
        self.assertEqual(balance.credit, 0)
        self.assertEqual(balance.net, 0)
        self.assertEqual(balance.debit, Decimal(19.99))

    # BalanceCoordinate

    def test_balance_coordinate_equality(self):
        balance_coordinate = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="GBP",
            phase=Phase.PENDING_OUT,
        )
        other_balance_coordinate = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="GBP",
            phase=Phase.PENDING_OUT,
        )

        self.assertEqual(balance_coordinate, other_balance_coordinate)
        self.assertEqual(
            balance_coordinate, (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_OUT)
        )

    def test_balance_coordinate_unequal_phase(self):
        balance_coordinate = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="GBP",
            phase=Phase.PENDING_OUT,
        )
        other_balance_coordinate = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="GBP",
            phase=Phase.COMMITTED,
        )

        self.assertNotEqual(balance_coordinate, other_balance_coordinate)

    # BalanceDefaultDict

    def test_balance_default_dict_equality(self):
        balance_default_dict = BalanceDefaultDict(
            default_dict=lambda *_: Balance(),
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            },
        )
        # Default dict doesn't affect equality
        other_balance_default_dict = BalanceDefaultDict(
            default_dict=lambda *_: Balance(credit=Decimal(4.2)),
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            },
        )

        self.assertEqual(balance_default_dict, other_balance_default_dict)

    def test_balance_default_dict_unequal_mapping(self):
        balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(1)
                )
            }
        )
        other_balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            }
        )

        self.assertNotEqual(balance_default_dict, other_balance_default_dict)

    # Shift, Override, Next, Previous

    def test_time_operations_equality(self):
        shift = Shift(years=3, months=1, days=12, hours=4, minutes=5, seconds=6)
        override = Override(year=2000, month=1, day=12)
        next = Next(month=1, day=12, hour=4, minute=5, second=6)
        previous = Previous(month=1, day=12, hour=6, minute=7, second=25)
        relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Next(month=1, day=12, hour=4, minute=5, second=6),
        )

        other_shift = Shift(years=3, months=1, days=12, hours=4, minutes=5, seconds=6)
        other_override = Override(year=2000, month=1, day=12)
        other_next = Next(month=1, day=12, hour=4, minute=5, second=6)
        other_previous = Previous(month=1, day=12, hour=6, minute=7, second=25)
        other_relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Next(month=1, day=12, hour=4, minute=5, second=6),
        )

        self.assertEqual(shift, other_shift)
        self.assertEqual(override, other_override)
        self.assertEqual(next, other_next)
        self.assertEqual(previous, other_previous)
        self.assertEqual(relative_date_time, other_relative_date_time)

    def test_time_operations_unequal_month(self):
        shift = Shift(years=3, months=1, days=12, hours=4, minutes=5, seconds=6)
        override = Override(year=2000, month=1, day=12)
        next = Next(month=1, day=12, hour=4, minute=5, second=6)
        previous = Previous(month=1, day=12, hour=6, minute=7, second=25)
        relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Next(month=1, day=12, hour=4, minute=5, second=6),
        )

        other_shift = Shift(years=3, months=2, days=12, hours=4, minutes=5, seconds=6)
        other_override = Override(year=2000, month=2, day=12)
        other_next = Next(month=2, day=12, hour=4, minute=5, second=6)
        other_previous = Previous(month=2, day=12, hour=6, minute=7, second=25)
        other_relative_date_time = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Next(month=2, day=12, hour=4, minute=5, second=6),
        )

        self.assertNotEqual(shift, other_shift)
        self.assertNotEqual(override, other_override)
        self.assertNotEqual(next, other_next)
        self.assertNotEqual(previous, other_previous)
        self.assertNotEqual(relative_date_time, other_relative_date_time)

    def test_shift_with_positive_values(self):
        shift = Shift(years=3, months=1, days=12, hours=4, minutes=5, seconds=6)
        self.assertEqual(3, shift.years)
        self.assertEqual(1, shift.months)
        self.assertEqual(12, shift.days)
        self.assertEqual(4, shift.hours)
        self.assertEqual(5, shift.minutes)
        self.assertEqual(6, shift.seconds)

    def test_shift_with_negative_values(self):
        shift = Shift(years=-4, months=-3, days=-2, hours=-10, minutes=-25, seconds=-45)
        self.assertEqual(-4, shift.years)
        self.assertEqual(-3, shift.months)
        self.assertEqual(-2, shift.days)
        self.assertEqual(-10, shift.hours)
        self.assertEqual(-25, shift.minutes)
        self.assertEqual(-45, shift.seconds)

    def test_shift_with_only_time_attribute_values(self):
        shift = Shift(hours=7, minutes=8, seconds=25)
        self.assertEqual(7, shift.hours)
        self.assertEqual(8, shift.minutes)
        self.assertEqual(25, shift.seconds)

    def test_shift_with_optional_values_not_provided(self):
        shift_missing_months = Shift(years=4, days=2, hours=-10, minutes=-25, seconds=-45)
        shift_missing_days = Shift(years=4, months=3, hours=-10, minutes=-25, seconds=-45)
        shift_missing_years = Shift(months=3, days=2, hours=-10, minutes=-25, seconds=-45)
        shift_missing_hours = Shift(years=4, months=3, days=2, minutes=25, seconds=45)
        shift_missing_minutes = Shift(years=2, days=2, months=3, hours=10, seconds=45)
        shift_missing_seconds = Shift(years=2, days=2, months=3, hours=10, minutes=25)

        # Confirm that values are populated with zero if left empty.
        self.assertEqual(None, shift_missing_years.years)
        self.assertEqual(None, shift_missing_months.months)
        self.assertEqual(None, shift_missing_days.days)
        self.assertEqual(None, shift_missing_hours.hours)
        self.assertEqual(None, shift_missing_minutes.minutes)
        self.assertEqual(None, shift_missing_seconds.seconds)

    def test_shift_repr(self):
        shift = Shift(years=2, months=3, days=-2, hours=-10, minutes=25, seconds=-45)
        expected = "Shift(years=2, months=3, days=-2, hours=-10, minutes=25, seconds=-45)"
        self.assertEqual(expected, repr(shift))

    def test_shift_raises_if_no_values_provided(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            Shift()

        self.assertEqual(
            str(e.exception), "Shift object needs to be populated with at least one attribute."
        )

    def test_shift_raises_if_invalid_year_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(years="1")
        self.assertEqual(
            str(e.exception), "'Shift.years' expected int if populated, got '1' of type str"
        )

    def test_shift_raises_if_invalid_month_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(months="1")
        self.assertEqual(
            str(e.exception), "'Shift.months' expected int if populated, got '1' of type str"
        )

    def test_shift_raises_if_invalid_day_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(days="1")
        self.assertEqual(
            str(e.exception), "'Shift.days' expected int if populated, got '1' of type str"
        )

    def test_shift_raises_if_invalid_hour_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(hours="1")
        self.assertEqual(
            str(e.exception), "'Shift.hours' expected int if populated, got '1' of type str"
        )

    def test_shift_raises_if_invalid_minute_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(minutes="1")
        self.assertEqual(
            str(e.exception), "'Shift.minutes' expected int if populated, got '1' of type str"
        )

    def test_shift_raises_if_invalid_second_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Shift(seconds="1")
        self.assertEqual(
            str(e.exception), "'Shift.seconds' expected int if populated, got '1' of type str"
        )

    def test_defined_date_time_enum(self):
        self.assertEqual(DefinedDateTime.LIVE.value, -1)
        self.assertEqual(DefinedDateTime.INTERVAL_START.value, 2)
        self.assertEqual(DefinedDateTime.EFFECTIVE_DATETIME.value, 3)
        with self.assertRaises(AttributeError):
            DefinedDateTime.EFFECTIVE_TIME

    def test_failover_enum(self):
        self.assertEqual(ScheduleFailover.FIRST_VALID_DAY_BEFORE.value, 1)
        self.assertEqual(ScheduleFailover.FIRST_VALID_DAY_AFTER.value, 2)

    def test_override_repr(self):
        override = Override(year=2000, month=1, day=12, hour=4, minute=5, second=6)
        expected = "Override(year=2000, month=1, day=12, hour=4, minute=5, second=6)"
        self.assertEqual(expected, repr(override))

    def test_override_with_valid_values(self):
        override = Override(year=2000, month=1, day=12, hour=4, minute=5, second=6)
        self.assertEqual(2000, override.year)
        self.assertEqual(1, override.month)
        self.assertEqual(12, override.day)
        self.assertEqual(4, override.hour)
        self.assertEqual(5, override.minute)
        self.assertEqual(6, override.second)

    def test_override_with_time_attributes_not_populated(self):
        override = Override(year=2000, month=1, day=12)
        self.assertEqual(2000, override.year)
        self.assertEqual(1, override.month)
        self.assertEqual(12, override.day)
        self.assertEqual(None, override.hour)
        self.assertEqual(None, override.minute)
        self.assertEqual(None, override.second)

    def test_override_with_optional_date_attribute_not_populated(self):
        override = Override(year=2000, day=12)
        self.assertEqual(2000, override.year)
        self.assertEqual(None, override.month)
        self.assertEqual(12, override.day)
        self.assertEqual(None, override.hour)
        self.assertEqual(None, override.minute)
        self.assertEqual(None, override.second)

    def test_override_raises_if_no_values_provided(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            Override()

        self.assertEqual(
            str(e.exception), "Override object needs to be populated with at least one attribute."
        )

    def test_override_raises_if_invalid_year_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(year="1")
        self.assertEqual(
            str(e.exception),
            "'Override.year' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_month_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(month="1")
        self.assertEqual(
            str(e.exception),
            "'Override.month' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_day_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(day="1")
        self.assertEqual(
            str(e.exception),
            "'Override.day' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_hour_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(hour="1")
        self.assertEqual(
            str(e.exception),
            "'Override.hour' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_minute_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(minute="1")
        self.assertEqual(
            str(e.exception),
            "'Override.minute' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_second_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(second="1")
        self.assertEqual(
            str(e.exception),
            "'Override.second' expected int if populated, got '1' of type str",
        )

    def test_override_raises_if_invalid_year_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(year=True)
        self.assertEqual(
            str(e.exception),
            "'Override.year' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_invalid_month_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(month=True)
        self.assertEqual(
            str(e.exception),
            "'Override.month' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_invalid_day_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(day=True)
        self.assertEqual(
            str(e.exception),
            "'Override.day' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_invalid_hour_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(hour=True)
        self.assertEqual(
            str(e.exception),
            "'Override.hour' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_invalid_minute_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(minute=True)
        self.assertEqual(
            str(e.exception),
            "'Override.minute' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_invalid_second_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Override(second=True)
        self.assertEqual(
            str(e.exception),
            "'Override.second' expected int if populated, got 'True' of type bool",
        )

    def test_override_raises_if_values_out_of_range(self):
        with self.assertRaises(InvalidSmartContractError) as ex1:
            Override(month=13)
        with self.assertRaises(InvalidSmartContractError) as ex2:
            Override(day=32)
        with self.assertRaises(InvalidSmartContractError) as ex3:
            Override(hour=24)
        with self.assertRaises(InvalidSmartContractError) as ex4:
            Override(minute=60)
        with self.assertRaises(InvalidSmartContractError) as ex5:
            Override(second=60)
        with self.assertRaises(InvalidSmartContractError) as ex6:
            Override(year=-1)
        with self.assertRaises(InvalidSmartContractError) as ex7:
            Override(month=0)
        with self.assertRaises(InvalidSmartContractError) as ex8:
            Override(day=0)
        with self.assertRaises(InvalidSmartContractError) as ex9:
            Override(hour=-1)
        with self.assertRaises(InvalidSmartContractError) as ex10:
            Override(minute=-1)
        with self.assertRaises(InvalidSmartContractError) as ex11:
            Override(second=-1)

        for ex in [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10, ex11]:
            self.assertEqual(str(ex.exception), "Values of Override object are out of range.")

    def test_next_with_all_values_not_provided(self):
        with self.assertRaises(TypeError) as e:
            Next()
        self.assertEqual(
            str(e.exception),
            "Next.__init__() missing 1 required keyword-only argument: 'day'",
        )

    def test_next_raises_if_invalid_month_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(month="1", day=1)
        self.assertEqual(
            str(e.exception), "'Next.month' expected int if populated, got '1' of type str"
        )

    def test_next_raises_if_invalid_day_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(day="1")
        self.assertEqual(str(e.exception), "'Next.day' expected int, got '1' of type str")

    def test_next_raises_if_invalid_hour_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(hour="1", day=1)
        self.assertEqual(
            str(e.exception), "'Next.hour' expected int if populated, got '1' of type str"
        )

    def test_next_raises_if_invalid_minute_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(minute="1", day=1)
        self.assertEqual(
            str(e.exception), "'Next.minute' expected int if populated, got '1' of type str"
        )

    def test_next_raises_if_invalid_second_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(second="1", day=1)
        self.assertEqual(
            str(e.exception), "'Next.second' expected int if populated, got '1' of type str"
        )

    def test_next_raises_if_invalid_month_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(month=True, day=1)
        self.assertEqual(
            str(e.exception), "'Next.month' expected int if populated, got 'True' of type bool"
        )

    def test_next_raises_if_invalid_day_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(day=True)
        self.assertEqual(str(e.exception), "'Next.day' expected int, got 'True' of type bool")

    def test_next_raises_if_invalid_hour_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(hour=True, day=1)
        self.assertEqual(
            str(e.exception), "'Next.hour' expected int if populated, got 'True' of type bool"
        )

    def test_next_raises_if_invalid_minute_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(minute=True, day=1)
        self.assertEqual(
            str(e.exception), "'Next.minute' expected int if populated, got 'True' of type bool"
        )

    def test_next_raises_if_invalid_second_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Next(second=True, day=1)
        self.assertEqual(
            str(e.exception), "'Next.second' expected int if populated, got 'True' of type bool"
        )

    def test_previous_with_all_values_not_provided(self):
        with self.assertRaises(TypeError) as e:
            Previous()
        self.assertEqual(
            str(e.exception),
            "Previous.__init__() missing 1 required keyword-only argument: 'day'",
        )

    def test_previous_raises_if_invalid_month_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(month="1", day=1)
        self.assertEqual(
            str(e.exception), "'Previous.month' expected int if populated, got '1' of type str"
        )

    def test_previous_raises_if_invalid_day_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(day="1")
        self.assertEqual(str(e.exception), "'Previous.day' expected int, got '1' of type str")

    def test_previous_raises_if_invalid_hour_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(hour="1", day=1)
        self.assertEqual(
            str(e.exception), "'Previous.hour' expected int if populated, got '1' of type str"
        )

    def test_previous_raises_if_invalid_minute_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(minute="1", day=1)
        self.assertEqual(
            str(e.exception), "'Previous.minute' expected int if populated, got '1' of type str"
        )

    def test_previous_raises_if_invalid_second_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(second="1", day=1)
        self.assertEqual(
            str(e.exception), "'Previous.second' expected int if populated, got '1' of type str"
        )

    def test_previous_raises_if_invalid_month_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(month=True, day=1)
        self.assertEqual(
            str(e.exception), "'Previous.month' expected int if populated, got 'True' of type bool"
        )

    def test_previous_raises_if_invalid_day_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(day=True)
        self.assertEqual(str(e.exception), "'Previous.day' expected int, got 'True' of type bool")

    def test_previous_raises_if_invalid_hour_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(hour=True, day=1)
        self.assertEqual(
            str(e.exception), "'Previous.hour' expected int if populated, got 'True' of type bool"
        )

    def test_previous_raises_if_invalid_minute_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(minute=True, day=1)
        self.assertEqual(
            str(e.exception),
            "'Previous.minute' expected int if populated, got 'True' of type " "bool",
        )

    def test_previous_raises_if_invalid_second_types_provided_bool(self):
        with self.assertRaises(StrongTypingError) as e:
            Previous(second=True, day=1)
        self.assertEqual(
            str(e.exception),
            "'Previous.second' expected int if populated, got 'True' of type " "bool",
        )

    def test_next_repr(self):
        next_native_type = Next(month=1, day=12, hour=4, minute=5, second=6)
        expected = "Next(month=1, day=12, hour=4, minute=5, second=6)"
        self.assertEqual(expected, repr(next_native_type))

    def test_next_with_all_values_populated(self):
        next_native_type = Next(month=1, day=12, hour=4, minute=5, second=6)
        self.assertEqual(1, next_native_type.month)
        self.assertEqual(12, next_native_type.day)
        self.assertEqual(4, next_native_type.hour)
        self.assertEqual(5, next_native_type.minute)
        self.assertEqual(6, next_native_type.second)

    def test_previous_repr(self):
        previous = Previous(month=5, day=17, hour=3, minute=45, second=12)
        expected = "Previous(month=5, day=17, hour=3, minute=45, second=12)"
        self.assertEqual(expected, repr(previous))

    def test_previous_with_all_values_populated(self):
        previous_native_type = Previous(month=5, day=17, hour=3, minute=45, second=12)
        self.assertEqual(5, previous_native_type.month)
        self.assertEqual(17, previous_native_type.day)
        self.assertEqual(3, previous_native_type.hour)
        self.assertEqual(45, previous_native_type.minute)
        self.assertEqual(12, previous_native_type.second)

    def test_next_raises_if_values_out_of_range(self):
        with self.assertRaises(InvalidSmartContractError) as ex1:
            Next(month=13, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex2:
            Next(day=32)
        with self.assertRaises(InvalidSmartContractError) as ex3:
            Next(hour=24, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex4:
            Next(minute=60, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex5:
            Next(second=60, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex6:
            Next(month=0, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex7:
            Next(day=0)

        for ex in [ex1, ex2, ex3, ex4, ex5, ex6, ex7]:
            self.assertEqual(str(ex.exception), "Values of Next object are out of range.")

    def test_previous_raises_if_values_out_of_range(self):
        with self.assertRaises(InvalidSmartContractError) as ex1:
            Previous(month=13, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex2:
            Previous(day=32)
        with self.assertRaises(InvalidSmartContractError) as ex3:
            Previous(hour=24, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex4:
            Previous(minute=60, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex5:
            Previous(second=60, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex6:
            Previous(month=0, day=2)
        with self.assertRaises(InvalidSmartContractError) as ex7:
            Previous(day=0)

        for ex in [ex1, ex2, ex3, ex4, ex5, ex6, ex7]:
            self.assertEqual(str(ex.exception), "Values of Previous object are out of range.")

    def test_relative_date_time_with_next(self):
        relative_date_time_native_object = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Next(month=1, day=12, hour=4, minute=5, second=6),
        )

        self.assertEqual(4, relative_date_time_native_object.shift.years)
        self.assertEqual(1, relative_date_time_native_object.shift.months)
        self.assertEqual(2, relative_date_time_native_object.shift.days)
        self.assertEqual(-10, relative_date_time_native_object.shift.hours)
        self.assertEqual(25, relative_date_time_native_object.shift.minutes)
        self.assertEqual(-45, relative_date_time_native_object.shift.seconds)

        self.assertEqual(1, relative_date_time_native_object.find.month)
        self.assertEqual(12, relative_date_time_native_object.find.day)
        self.assertEqual(4, relative_date_time_native_object.find.hour)
        self.assertEqual(5, relative_date_time_native_object.find.minute)
        self.assertEqual(6, relative_date_time_native_object.find.second)

        self.assertEqual(
            DefinedDateTime.EFFECTIVE_DATETIME, relative_date_time_native_object.origin
        )

    def test_relative_date_time_with_previous(self):
        relative_date_time_native_object = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Previous(month=1, day=12, hour=6, minute=7, second=25),
        )

        self.assertEqual(4, relative_date_time_native_object.shift.years)
        self.assertEqual(1, relative_date_time_native_object.shift.months)
        self.assertEqual(2, relative_date_time_native_object.shift.days)
        self.assertEqual(-10, relative_date_time_native_object.shift.hours)
        self.assertEqual(25, relative_date_time_native_object.shift.minutes)
        self.assertEqual(-45, relative_date_time_native_object.shift.seconds)

        self.assertEqual(1, relative_date_time_native_object.find.month)
        self.assertEqual(12, relative_date_time_native_object.find.day)
        self.assertEqual(6, relative_date_time_native_object.find.hour)
        self.assertEqual(7, relative_date_time_native_object.find.minute)
        self.assertEqual(25, relative_date_time_native_object.find.second)

        self.assertEqual(
            DefinedDateTime.EFFECTIVE_DATETIME, relative_date_time_native_object.origin
        )

    def test_relative_date_time_raises_if_invalid_shift_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            RelativeDateTime(shift="1", origin=DefinedDateTime.EFFECTIVE_DATETIME)
        self.assertEqual(
            str(e.exception),
            "'RelativeDateTime.shift' expected Shift if populated, got '1' of type str",
        )

    def test_relative_date_time_raises_if_invalid_find_types_provided(self):
        with self.assertRaises(StrongTypingError) as e:
            RelativeDateTime(find="1", origin=DefinedDateTime.EFFECTIVE_DATETIME)
        self.assertEqual(
            str(e.exception),
            "'RelativeDateTime.find' expected Union[Next, Previous, Override] if populated, got "
            "'1' of type str",
        )

    def test_relative_date_time_with_shift_and_find_not_populated(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            RelativeDateTime(origin=DefinedDateTime.EFFECTIVE_DATETIME)

        self.assertEqual(
            str(ex.exception),
            "RelativeDateTime Object requires either shift or find attributes to be populated",
        )

    def test_relative_date_time_repr(self):
        relative_date_time_native_object = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Override(year=2, month=1, day=12, hour=2, minute=9, second=53),
        )
        expected = (
            "RelativeDateTime(origin=DefinedDateTime.EFFECTIVE_DATETIME, "
            + "shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45), "
            + "find=Override(year=2, month=1, day=12, hour=2, minute=9, second=53))"
        )
        self.assertEqual(expected, repr(relative_date_time_native_object))

    def test_relative_date_time_with_override(self):
        relative_date_time_native_object = RelativeDateTime(
            origin=DefinedDateTime.EFFECTIVE_DATETIME,
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Override(year=2, month=1, day=12, hour=2, minute=9, second=53),
        )

        self.assertEqual(4, relative_date_time_native_object.shift.years)
        self.assertEqual(1, relative_date_time_native_object.shift.months)
        self.assertEqual(2, relative_date_time_native_object.shift.days)
        self.assertEqual(-10, relative_date_time_native_object.shift.hours)
        self.assertEqual(25, relative_date_time_native_object.shift.minutes)
        self.assertEqual(-45, relative_date_time_native_object.shift.seconds)

        self.assertEqual(2, relative_date_time_native_object.find.year)
        self.assertEqual(1, relative_date_time_native_object.find.month)
        self.assertEqual(12, relative_date_time_native_object.find.day)
        self.assertEqual(2, relative_date_time_native_object.find.hour)
        self.assertEqual(9, relative_date_time_native_object.find.minute)
        self.assertEqual(53, relative_date_time_native_object.find.second)

        self.assertEqual(
            DefinedDateTime.EFFECTIVE_DATETIME, relative_date_time_native_object.origin
        )

    def test_relative_date_time_with_origin_interval_start(self):
        relative_date_time_native_object = RelativeDateTime(
            shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
            find=Override(year=2, month=1, day=12, hour=2, minute=9, second=53),
            origin=DefinedDateTime.INTERVAL_START,
        )

        self.assertEqual(4, relative_date_time_native_object.shift.years)
        self.assertEqual(1, relative_date_time_native_object.shift.months)
        self.assertEqual(2, relative_date_time_native_object.shift.days)
        self.assertEqual(-10, relative_date_time_native_object.shift.hours)
        self.assertEqual(25, relative_date_time_native_object.shift.minutes)
        self.assertEqual(-45, relative_date_time_native_object.shift.seconds)

        self.assertEqual(2, relative_date_time_native_object.find.year)
        self.assertEqual(1, relative_date_time_native_object.find.month)
        self.assertEqual(12, relative_date_time_native_object.find.day)
        self.assertEqual(2, relative_date_time_native_object.find.hour)
        self.assertEqual(9, relative_date_time_native_object.find.minute)
        self.assertEqual(53, relative_date_time_native_object.find.second)

        self.assertEqual(DefinedDateTime.INTERVAL_START, relative_date_time_native_object.origin)

    def test_relative_date_time_with_origin_using_illegal_live_value(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            RelativeDateTime(
                shift=Shift(years=4, months=1, days=2, hours=-10, minutes=25, seconds=-45),
                find=Override(year=2, month=1, day=12, hour=2, minute=9, second=53),
                origin=DefinedDateTime.LIVE,
            )
        self.assertEqual(
            str(ex.exception),
            "RelativeDateTime origin attribute does not support 'DefinedDateTime.LIVE'",
        )

    # BalancesObservation

    def test_balances_observation(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        balance_key_1 = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="USD",
            phase=Phase.COMMITTED,
        )
        balance_dict = BalanceDefaultDict()
        balance_dict[balance_key_1] = Balance(net=Decimal("20"), credit=Decimal("20"))
        balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=balance_dict
        )
        self.assertEqual(balance_dict, balances_observation.balances)
        self.assertEqual(value_datetime, balances_observation.value_datetime)

    def test_balances_observation_equality(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            }
        )
        other_balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            }
        )

        balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=balance_default_dict
        )
        other_balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=other_balance_default_dict
        )

        self.assertEqual(balances_observation, other_balances_observation)

    def test_balances_observation_unequal_balances(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(5.50)
                )
            }
        )
        other_balance_default_dict = BalanceDefaultDict(
            mapping={
                (DEFAULT_ADDRESS, DEFAULT_ASSET, "GBP", Phase.PENDING_IN): Balance(
                    credit=Decimal(1)
                )
            }
        )

        balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=balance_default_dict
        )
        other_balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=other_balance_default_dict
        )

        self.assertNotEqual(balances_observation, other_balances_observation)

    def test_balances_observation_repr(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("UTC"))
        balance_key_1 = BalanceCoordinate(
            account_address=DEFAULT_ADDRESS,
            asset=DEFAULT_ASSET,
            denomination="USD",
            phase=Phase.COMMITTED,
        )
        balance_dict = BalanceDefaultDict()
        balance_dict[balance_key_1] = Balance(net=Decimal("20"), credit=Decimal("20"))
        balances_observation = BalancesObservation(
            value_datetime=value_datetime, balances=balance_dict
        )
        expected = (
            "BalancesObservation("
            + "value_datetime=datetime.datetime(2020, 2, 20, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "balances={BalanceCoordinate(account_address='DEFAULT', asset='COMMERCIAL_BANK_MONEY', "
            + "denomination='USD', phase=Phase.COMMITTED): Balance(credit=Decimal('20'), "
            + "debit=Decimal('0'), net=Decimal('20'))})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(balances_observation))

    def test_balances_observation_raises_with_wrong_balances_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesObservation(balances=None)
        self.assertEqual(
            str(e.exception),
            "'BalancesObservation.balances' expected BalanceDefaultDict, got None",
        )

    def test_balances_observation_raises_with_naive_datetime(self):
        value_datetime = datetime(year=2020, month=2, day=20)
        balance_dict = BalanceDefaultDict()
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservation(value_datetime=value_datetime, balances=balance_dict)
        self.assertEqual(
            str(e.exception),
            "'value_datetime' of BalancesObservation is not timezone aware.",
        )

    def test_balances_observation_raises_with_non_utc_timezone(self):
        value_datetime = datetime(year=2020, month=2, day=20, tzinfo=ZoneInfo("US/Pacific"))
        balance_dict = BalanceDefaultDict()
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservation(value_datetime=value_datetime, balances=balance_dict)
        self.assertEqual(
            str(e.exception),
            "'value_datetime' of BalancesObservation must have timezone UTC, currently "
            "US/Pacific.",
        )

    def test_balances_observation_raises_with_non_zoneinfo_timezone(self):
        value_datetime = datetime.fromtimestamp(1, timezone.utc)
        balance_dict = BalanceDefaultDict()
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesObservation(value_datetime=value_datetime, balances=balance_dict)
        self.assertEqual(
            "'value_datetime' of BalancesObservation must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(e.exception),
        )

    def test_balances_observation_no_value_datetime_and_empty_balances(self):
        balance_dict = BalanceDefaultDict()
        balances_observation = BalancesObservation(value_datetime=None, balances=balance_dict)
        self.assertEqual(None, balances_observation.value_datetime)
        self.assertEqual(balance_dict, balances_observation.balances)

    # ParametersFilter

    def test_parameters_filter_repr(self):
        filter = ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_2"])
        expected = "ParametersFilter(parameter_ids=['PARAMETER_1', 'PARAMETER_2'])"
        self.assertEquals(expected, repr(filter))

    def test_parameters_filter(self):
        parameter_ids = ["PARAMETER_1", "PARAMETER_2"]
        parameters_filter = ParametersFilter(parameter_ids=parameter_ids)
        self.assertEqual(parameter_ids, parameters_filter.parameter_ids)

    def test_parameters_filter_equality(self):
        parameter_ids = ["PARAMETER_1", "PARAMETER_2"]
        parameters_filter = ParametersFilter(parameter_ids=parameter_ids)
        other_parameter_ids = ["PARAMETER_1", "PARAMETER_2"]
        other_parameters_filter = ParametersFilter(parameter_ids=other_parameter_ids)

        self.assertEqual(parameters_filter, other_parameters_filter)

    def test_parameters_filter_unequal_parameter_ids(self):
        parameter_ids = ["PARAMETER_1", "PARAMETER_2"]
        parameters_filter = ParametersFilter(parameter_ids=parameter_ids)
        other_parameter_ids = ["PARAMETER_1", "PARAMETER_42"]
        other_parameters_filter = ParametersFilter(parameter_ids=other_parameter_ids)

        self.assertNotEqual(parameters_filter, other_parameters_filter)

    def test_parameters_filter_with_empty_parameter_ids(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersFilter(parameter_ids=[])
        self.assertEqual(
            str(e.exception),
            "'ParametersFilter.parameter_ids' must be a non empty list, got []",
        )

    def test_parameters_filter_with_empty_parameter_id_field(self):
        with self.assertRaises(TypeError) as e:
            ParametersFilter()
        self.assertEqual(
            str(e.exception),
            "ParametersFilter.__init__() missing 1 "
            "required keyword-only argument: 'parameter_ids'",
        )

    def test_parameters_filter_with_duplicate_parameter_ids(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersFilter(parameter_ids=["PARAMETER_1", "PARAMETER_1"])
        self.assertEqual(
            str(e.exception),
            "ParametersFilter parameter_ids must not contain any duplicate parameter ids.",
        )

    def test_parameters_filter_invalid_argument_type(self):
        with self.assertRaises(StrongTypingError):
            ParametersFilter(parameter_ids=123)

    # ParametersObservation

    def test_parameters_observation(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        self.assertEqual(parameters, parameters_observation.parameters)
        self.assertEqual(value_datetime, parameters_observation.value_datetime)

    def test_parameters_observation_repr(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        expected = (
            "ParametersObservation(parameters={'parameter_1': 'string_value', "
            + "'parameter_2': Decimal('3.14159')}, value_datetime="
            + "datetime.datetime(2020, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))"
        )
        self.assertEqual(expected, repr(parameters_observation))

    def test_parameters_observation_equality(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        other_parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        self.assertEqual(parameters_observation, other_parameters_observation)

    def test_parameters_observation_unequal_parameters(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        other_parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.1"),
        }
        other_parameters_observation = ParametersObservation(
            parameters=other_parameters,
            value_datetime=value_datetime,
        )
        self.assertNotEqual(parameters_observation, other_parameters_observation)

    def test_parameters_observation_empty_parameters(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {}
        parameters_observation = ParametersObservation(
            parameters=parameters,
            value_datetime=value_datetime,
        )
        self.assertEqual(parameters, parameters_observation.parameters)
        self.assertEqual(value_datetime, parameters_observation.value_datetime)

    def test_parameters_observation_raises_with_naive_value_datetime(self):
        value_datetime = datetime(year=2020, month=1, day=1)
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            str(e.exception),
            "'value_datetime' of ParametersObservation is not timezone aware.",
        )

    def test_parameters_observation_raises_with_non_utc_timezone(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("US/Pacific"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            str(e.exception),
            "'value_datetime' of ParametersObservation must have timezone UTC, currently US/Pacific.",  # noqa: E501
        )

    def test_parameters_observation_raises_with_non_zoneinfo_timezone(self):
        value_datetime = datetime.fromtimestamp(1, timezone.utc)
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": Decimal("3.14159"),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            "'value_datetime' of ParametersObservation must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(e.exception),
        )

    def test_parameters_observation_raises_with_naive_datetime_parameters(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": datetime(2022, 1, 1),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            str(e.exception),
            "'parameters[\"parameter_2\"]' of ParametersObservation is not timezone aware.",
        )

    def test_parameters_observation_raises_with_non_utc_timezone_datetime_parameters(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": datetime(2022, 1, 1, tzinfo=ZoneInfo("US/Pacific")),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            str(e.exception),
            "'parameters[\"parameter_2\"]' of ParametersObservation must have timezone UTC, currently US/Pacific.",  # noqa: E501
        )

    def test_parameters_observation_raises_with_non_zoneinfo_timezone_datetime_parameters(self):
        value_datetime = datetime(year=2020, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        parameters = {
            "parameter_1": "string_value",
            "parameter_2": datetime.fromtimestamp(1, timezone.utc),
        }
        with self.assertRaises(InvalidSmartContractError) as e:
            ParametersObservation(
                parameters=parameters,
                value_datetime=value_datetime,
            )
        self.assertEqual(
            "'parameters[\"parameter_2\"]' of ParametersObservation must have timezone of type ZoneInfo, currently <class 'datetime.timezone'>.",  # noqa: E501
            str(e.exception),
        )

    # ScheduledEvent

    def test_scheduled_event(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")
        skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=skip,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)
        self.assertEqual(skip, scheduled_event.skip)

    def test_scheduled_event_equality(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")
        skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )
        other_schedule_expression = ScheduleExpression(day="5")
        other_skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=skip,
        )
        other_scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=other_schedule_expression,
            skip=other_skip,
        )

        self.assertEqual(scheduled_event, other_scheduled_event)

    def test_scheduled_event_unequal_expression(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")
        skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )
        other_schedule_expression = ScheduleExpression(day="10")
        other_skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=skip,
        )
        other_scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=other_schedule_expression,
            skip=other_skip,
        )

        self.assertNotEqual(scheduled_event, other_scheduled_event)

    def test_scheduled_event_unequal_skip(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")
        skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
        )
        other_schedule_expression = ScheduleExpression(day="5")
        other_skip = ScheduleSkip(
            end=datetime(year=2000, month=1, day=24, tzinfo=ZoneInfo("UTC")),
        )

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=skip,
        )
        other_scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=other_schedule_expression,
            skip=other_skip,
        )

        self.assertNotEqual(scheduled_event, other_scheduled_event)

    def test_scheduled_event_repr(self):
        scheduled_event = ScheduledEvent(
            start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
            end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
            expression=ScheduleExpression(day="5"),
            skip=ScheduleSkip(
                end=datetime(year=2000, month=1, day=20, tzinfo=ZoneInfo("UTC")),
            ),
        )
        expected = (
            "ScheduledEvent(start_datetime="
            + "datetime.datetime(2000, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "end_datetime=datetime.datetime"
            + "(2000, 2, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), "
            + "expression=ScheduleExpression(day='5', day_of_week=None, hour=None, "
            + "minute=None, second=None, month=None, year=None), "
            + "schedule_method=None, "
            + "skip=ScheduleSkip(end=datetime.datetime(2000, 1, 20, 0, 0, "
            + "tzinfo=zoneinfo.ZoneInfo(key='UTC'))))"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(scheduled_event))

    def test_scheduled_event_raises_with_naive_start_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEvent(
                start_datetime=datetime(2022, 1, 1),
            )
        self.assertEqual(
            "'start_datetime' of ScheduledEvent is not timezone aware.",
            str(ex.exception),
        )

    def test_scheduled_event_raises_with_naive_end_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(2022, 1, 1),
            )
        self.assertEqual(
            "'end_datetime' of ScheduledEvent is not timezone aware.",
            str(ex.exception),
        )

    def test_scheduled_event_raises_with_naive_skip_end_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            ScheduledEvent(
                start_datetime=datetime(1970, 1, 1, second=1, tzinfo=ZoneInfo("UTC")),
                skip=ScheduleSkip(
                    end=datetime(year=2000, month=1, day=20),
                ),
            )
        self.assertEqual(
            "'end' of ScheduleSkip is not timezone aware.",
            str(ex.exception),
        )

    def test_scheduled_event_schedule_method(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_method = EndOfMonthSchedule(day=5)

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            schedule_method=schedule_method,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_method, scheduled_event.schedule_method)

    def test_scheduled_event_with_no_start_end_datetimes(self):
        schedule_expression = ScheduleExpression(day="5")
        scheduled_event = ScheduledEvent(expression=schedule_expression)
        self.assertEqual(None, scheduled_event.start_datetime)
        self.assertEqual(None, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)

    def test_scheduled_event_invalid_start_datetime_raises(self):
        with self.assertRaises(StrongTypingError) as e:
            ScheduledEvent(
                start_datetime=True,
                end_datetime=datetime(year=2000, month=2, day=1),
                expression=ScheduleExpression(day="5"),
            )
        self.assertEqual(
            "'ScheduledEvent.start_datetime' expected datetime if populated, "
            "got 'True' of type bool",
            str(e.exception),
        )

    def test_scheduled_event_no_end_datetime(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            expression=schedule_expression,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(None, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)

    def test_scheduled_event_invalid_end_datetime_raises(self):
        with self.assertRaises(StrongTypingError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=True,
                expression=ScheduleExpression(day="5"),
            )
        self.assertEqual(
            "'ScheduledEvent.end_datetime' expected datetime if populated, got 'True' of type "
            "bool",
            str(e.exception),
        )

    def test_scheduled_event_no_end_datetime_expression_schedule_method_or_skip_raises(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "ScheduledEvent must have an end_datetime, expression, schedule_method or skip set",
            str(e.exception),
        )

    def test_scheduled_event_expression_and_schedule_method_raises(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
                schedule_method=EndOfMonthSchedule(day=5),
            )
        self.assertEqual(
            "ScheduledEvent must not have both expression and schedule_method set",
            str(e.exception),
        )

    def test_scheduled_event_with_skip_expression_and_schedule_method_raises(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
                schedule_method=EndOfMonthSchedule(day=5),
                skip=True,
            )
        self.assertEqual(
            "ScheduledEvent must not have both expression and schedule_method set",
            str(e.exception),
        )

    def test_scheduled_event_invalid_expression_raises(self):
        with self.assertRaises(StrongTypingError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                expression=True,
            )
        self.assertEqual(
            "'ScheduledEvent.expression' expected ScheduleExpression if populated, got 'True' of "
            "type bool",
            str(e.exception),
        )

    def test_scheduled_event_invalid_schedule_method_raises(self):
        with self.assertRaises(StrongTypingError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                schedule_method=True,
            )
        self.assertEqual(
            "'ScheduledEvent.schedule_method' expected EndOfMonthSchedule if populated, got "
            "'True' of type bool",
            str(e.exception),
        )

    def test_scheduled_event_no_skip(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)

    def test_scheduled_event_invalid_skip_raises(self):
        with self.assertRaises(StrongTypingError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                expression=ScheduleExpression(day="5"),
                skip="not-a-skip",
            )
        self.assertEqual(
            "'ScheduledEvent.skip' expected Union[bool, ScheduleSkip] if populated, got "
            "'not-a-skip' of type str",
            str(e.exception),
        )

    def test_scheduled_event_indefinite_skip(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=True,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)
        self.assertEqual(True, scheduled_event.skip)

    def test_scheduled_event_unskip(self):
        start_datetime = datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC"))
        end_datetime = datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC"))
        schedule_expression = ScheduleExpression(day="5")

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            skip=False,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)
        self.assertEqual(False, scheduled_event.skip)

    def test_scheduled_event_from_proto_skips_validation(self):
        start_datetime = "not-datetime"
        end_datetime = 2022
        schedule_expression = True
        schedule_method = "not-end-of-month-schedule"

        scheduled_event = ScheduledEvent(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            expression=schedule_expression,
            schedule_method=schedule_method,
            _from_proto=True,
        )
        self.assertEqual(start_datetime, scheduled_event.start_datetime)
        self.assertEqual(end_datetime, scheduled_event.end_datetime)
        self.assertEqual(schedule_expression, scheduled_event.expression)

    def test_scheduled_event_not_exactly_one_of_expression_and_schedule_method_raises(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "ScheduledEvent must have exactly one of expression or schedule_method set",
            str(e.exception),
        )

    def test_scheduled_event_with_skip_not_exactly_one_of_expression_and_schedule_method_raises_(
        self,
    ):
        with self.assertRaises(InvalidSmartContractError) as e:
            ScheduledEvent(
                start_datetime=datetime(year=2000, month=1, day=1, tzinfo=ZoneInfo("UTC")),
                end_datetime=datetime(year=2000, month=2, day=1, tzinfo=ZoneInfo("UTC")),
                skip=True,
            )
        self.assertEqual(
            "ScheduledEvent must have exactly one of expression or schedule_method set",
            str(e.exception),
        )

    # EndOfMonthSchedule

    def test_end_of_month_schedule_type_default_values(self):
        end_of_month_schedule = EndOfMonthSchedule(day=1)
        self.assertEqual(0, end_of_month_schedule.hour)
        self.assertEqual(0, end_of_month_schedule.minute)
        self.assertEqual(0, end_of_month_schedule.second)
        self.assertEqual(ScheduleFailover.FIRST_VALID_DAY_BEFORE, end_of_month_schedule.failover)

    def test_end_of_month_schedule_repr(self):
        end_of_month_schedule = EndOfMonthSchedule(day=1)
        expected = (
            "EndOfMonthSchedule(day=1, hour=0, minute=0, second=0, "
            + "failover=ScheduleFailover.FIRST_VALID_DAY_BEFORE)"
        )
        self.assertEqual(expected, repr(end_of_month_schedule))

    def test_end_of_month_schedule_equality(self):
        end_of_month_schedule = EndOfMonthSchedule(day=1)
        other_end_of_month_schedule = EndOfMonthSchedule(day=1)
        self.assertEqual(end_of_month_schedule, other_end_of_month_schedule)

    def test_end_of_month_schedule_unequal_day(self):
        end_of_month_schedule = EndOfMonthSchedule(day=1)
        other_end_of_month_schedule = EndOfMonthSchedule(day=24)
        self.assertNotEqual(end_of_month_schedule, other_end_of_month_schedule)

    def test_end_of_month_schedule_type_can_set_values(self):
        end_of_month_schedule = EndOfMonthSchedule(
            day=15, hour=10, minute=20, second=5, failover=ScheduleFailover.FIRST_VALID_DAY_BEFORE
        )
        self.assertEqual(15, end_of_month_schedule.day)
        self.assertEqual(10, end_of_month_schedule.hour)
        self.assertEqual(20, end_of_month_schedule.minute)
        self.assertEqual(5, end_of_month_schedule.second)
        self.assertEqual(ScheduleFailover.FIRST_VALID_DAY_BEFORE, end_of_month_schedule.failover)

    def test_end_of_month_schedule_raise_if_values_out_of_range(self):
        values = [
            {"day": 0},
            {"day": 32},
            {"day": 1, "hour": -1},
            {"day": 1, "hour": 25},
            {"day": 1, "minute": -1},
            {"day": 1, "minute": 61},
            {"day": 1, "second": -1},
            {"day": 1, "second": 61},
        ]

        error_parts = [
            ("day", 1, 31),
            ("day", 1, 31),
            ("hour", 0, 23),
            ("hour", 0, 23),
            ("minute", 0, 59),
            ("minute", 0, 59),
            ("second", 0, 59),
            ("second", 0, 59),
        ]

        for i, value in enumerate(values):
            time_component, low, high = error_parts[i]
            with self.assertRaises(InvalidSmartContractError) as e:
                EndOfMonthSchedule(**value)
            self.assertEqual(
                str(e.exception),
                f"Argument {time_component} of EndOfMonthSchedule"
                f" object is out of range({low}-{high}).",
            )

    # DateTimeConstraint

    def test_date_time_constraint_repr(self):
        constraint = DateTimeConstraint(precision=DateTimePrecision.DAY)
        expected = "DateTimeConstraint(precision=DateTimePrecision.DAY, earliest=None, latest=None)"
        self.assertEqual(expected, repr(constraint))

    def test_date_time_constraint_equality(self):
        constraint = DateTimeConstraint(precision=DateTimePrecision.DAY)
        other_constraint = DateTimeConstraint(precision=DateTimePrecision.DAY)

        self.assertEqual(constraint, other_constraint)

    def test_date_time_constraint_unequal_precision(self):
        constraint = DateTimeConstraint(precision=DateTimePrecision.DAY)
        other_constraint = DateTimeConstraint(precision=DateTimePrecision.MINUTE)

        self.assertNotEqual(constraint, other_constraint)

    def test_date_time_constraint_requires_precision_argument(self):
        with self.assertRaises(StrongTypingError) as ex:
            DateTimeConstraint(precision="")
        self.assertEqual(
            "'precision' expected DateTimePrecision value, got '' of type str", str(ex.exception)
        )

    def test_date_time_constraint_invalid_precision(self):
        with self.assertRaises(StrongTypingError) as ex:
            DateTimeConstraint(precision=27)
        expected = "'precision' expected DateTimePrecision value, got '27' of type int"
        self.assertEqual(expected, str(ex.exception))

    def test_date_time_constraint_stores_valid_arguments(self):
        earliest_datetime = datetime.fromtimestamp(1).replace(tzinfo=ZoneInfo("UTC"))
        latest_datetime = datetime.fromtimestamp(2).replace(tzinfo=ZoneInfo("UTC"))
        constraint = DateTimeConstraint(
            precision=DateTimePrecision.MINUTE,
            earliest=earliest_datetime,
            latest=latest_datetime,
        )
        self.assertEqual(DateTimePrecision.MINUTE, constraint.precision)
        self.assertEqual(earliest_datetime, constraint.earliest)
        self.assertEqual(latest_datetime, constraint.latest)

    def test_date_time_constraint_raises_with_naive_earliest_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateTimeConstraint(
                precision=DateTimePrecision.MINUTE,
                earliest=datetime.fromtimestamp(1),
            )
        expected = "'earliest' of DateTimeConstraint is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_date_time_constraint_raises_with_naive_latest_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateTimeConstraint(
                precision=DateTimePrecision.MINUTE,
                latest=datetime.fromtimestamp(1),
            )
        expected = "'latest' of DateTimeConstraint is not timezone aware."
        self.assertEqual(expected, str(ex.exception))

    def test_date_time_constraint_raises_with_non_utc_earliest_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateTimeConstraint(
                precision=DateTimePrecision.MINUTE,
                earliest=datetime.fromtimestamp(1).replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'earliest' of DateTimeConstraint must have timezone UTC, currently US/Pacific."
        self.assertEqual(expected, str(ex.exception))

    def test_date_time_constraint_raises_with_non_utc_latest_datetime(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            DateTimeConstraint(
                precision=DateTimePrecision.MINUTE,
                latest=datetime.fromtimestamp(1).replace(tzinfo=ZoneInfo("US/Pacific")),
            )
        expected = "'latest' of DateTimeConstraint must have timezone UTC, currently US/Pacific."
        self.assertEqual(expected, str(ex.exception))

    def test_date_time_constraint_rejects_earliest_after_latest(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            DateTimeConstraint(
                precision=DateTimePrecision.MINUTE,
                earliest=datetime.fromtimestamp(10, timezone.utc).replace(tzinfo=ZoneInfo("UTC")),
                latest=datetime.fromtimestamp(1, timezone.utc).replace(tzinfo=ZoneInfo("UTC")),
            )
        self.assertEqual(
            "DateTimeConstraint earliest must be no later than latest "
            "(received 1970-01-01 00:00:10+00:00 > 1970-01-01 00:00:01+00:00)",
            str(e.exception),
        )

    def test_date_time_constraint_raises_with_invalid_date(self):
        with self.assertRaises(StrongTypingError) as ex:
            DateTimeConstraint(precision=DateTimePrecision.MINUTE, earliest="today")
        self.assertEqual("'earliest' expected datetime, got 'today' of type str", str(ex.exception))

    def test_date_time_constraint_default_precision(self):
        constraint = DateTimeConstraint()
        self.assertEqual(None, constraint.precision)

    # DecimalConstraint

    def test_decimal_constraint_repr(self):
        constraint = DecimalConstraint(
            min_value=Decimal("1.2"),
            max_value=Decimal("123.4"),
        )
        expected = "DecimalConstraint(min_value=Decimal('1.2'), max_value=Decimal('123.4'))"
        self.assertEqual(expected, repr(constraint))

    def test_decimal_constraint_equality(self):
        constraint = DecimalConstraint(
            min_value=Decimal("1.2"),
            max_value=Decimal("123.4"),
        )
        other_constraint = DecimalConstraint(
            min_value=Decimal("1.2"),
            max_value=Decimal("123.4"),
        )
        self.assertEqual(constraint, other_constraint)

    def test_decimal_constraint_unequal_min_value(self):
        constraint = DecimalConstraint(
            min_value=Decimal("1.2"),
            max_value=Decimal("123.4"),
        )
        other_constraint = DecimalConstraint(
            min_value=Decimal("4.2"),
            max_value=Decimal("123.4"),
        )
        self.assertNotEqual(constraint, other_constraint)

    def test_decimal_constraint_stores_valid_arguments(self):
        constraint = DecimalConstraint(
            min_value=Decimal("1.2"),
            max_value=Decimal("123.4"),
        )
        self.assertEqual(Decimal("1.2"), constraint.min_value)
        self.assertEqual(Decimal("123.4"), constraint.max_value)

    def test_decimal_constraint_rejects_min_greater_than_max(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            DecimalConstraint(min_value=Decimal("10"), max_value=Decimal("9"))
        expected = (
            "DecimalConstraint 'min_value' must be less than or equal to 'max_value' "
            "(received 10 > 9)"
        )
        self.assertEqual(expected, str(e.exception))

    # EnumerationConstraint

    def test_enumeration_constraint_repr(self):
        constraint = EnumerationConstraint(permitted_values=["value-1", "value-2"])
        expected = "EnumerationConstraint(permitted_values=['value-1', 'value-2'])"
        self.assertEqual(expected, repr(constraint))

    def test_enumeration_constraint_equality(self):
        constraint = EnumerationConstraint(permitted_values=["value-1", "value-2"])
        other_constraint = EnumerationConstraint(permitted_values=["value-1", "value-2"])

        self.assertEqual(constraint, other_constraint)

    def test_enumeration_constraint_unequal_permitted_values(self):
        constraint = EnumerationConstraint(permitted_values=["value-1", "value-2"])
        other_constraint = EnumerationConstraint(permitted_values=["value-1", "value-3"])

        self.assertNotEqual(constraint, other_constraint)

    def test_enumeration_constraint_requires_permitted_values(self):
        with self.assertRaises(TypeError) as e:
            EnumerationConstraint()
        self.assertEqual(
            "EnumerationConstraint.__init__() missing 1 required "
            "keyword-only argument: 'permitted_values'",
            str(e.exception),
        )

    def test_enumeration_constraint_stores_valid_argument(self):
        constraint = EnumerationConstraint(permitted_values=["value-1", "value-2"])
        self.assertEqual(["value-1", "value-2"], constraint.permitted_values)

    def test_enumeration_constraint_from_proto_requires_list(self):
        with self.assertRaises(StrongTypingError) as e:
            EnumerationConstraint(permitted_values="not a list")
        self.assertEqual(
            "'permitted_values' expected list, got 'not a list' of type str", str(e.exception)
        )

    # AccountConstraint

    def test_account_constraint_repr(self):
        constraint = AccountConstraint()
        expected = "AccountConstraint()"
        self.assertEqual(expected, repr(constraint))

    def test_account_constraint_equality(self):
        constraint = AccountConstraint()
        other_constraint = AccountConstraint()

        self.assertEqual(constraint, other_constraint)

    # StringConstraint

    def test_string_constraint_repr(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        expected = "StringConstraint(min_length=1, max_length=10)"
        self.assertEqual(expected, repr(constraint))

    def test_string_constraint_equality(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        other_constraint = StringConstraint(min_length=1, max_length=10)

        self.assertEqual(constraint, other_constraint)

    def test_string_constraint_unequal_min_length(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        other_constraint = StringConstraint(min_length=4, max_length=10)

        self.assertNotEqual(constraint, other_constraint)

    def test_string_constraint_accepts_no_arguments(self):
        constraint = StringConstraint()
        self.assertEqual(0, constraint.min_length)
        self.assertEqual(0, constraint.max_length)

    def test_string_constraint_accepts_none(self):
        constraint = StringConstraint(min_length=None, max_length=None)
        self.assertEqual(0, constraint.min_length)
        self.assertEqual(0, constraint.max_length)

    def test_string_constraint_stores_valid_arguments(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        self.assertEqual(1, constraint.min_length)
        self.assertEqual(10, constraint.max_length)

    def test_string_constraint_stores_raises_invalid_argument(self):
        with self.assertRaises(StrongTypingError) as ex:
            StringConstraint(min_length=1, max_length="not a number")
        self.assertEqual("Expected int, got 'not a number' of type str", str(ex.exception))

    def test_string_constraint_rejects_negative_min_length(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            StringConstraint(min_length=-1, max_length=10)
        self.assertEqual(
            "StringConstraint min_length must be non-negative (received -1)", str(e.exception)
        )

    def test_string_constraint_rejects_negative_max_length(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            StringConstraint(min_length=1, max_length=-10)
        self.assertEqual(
            "StringConstraint max_length must be non-negative (received -10)", str(e.exception)
        )

    def test_string_constraint_rejects_empty_interval(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            StringConstraint(min_length=11, max_length=10)
        self.assertEqual(
            "StringConstraint min_length must be less than or equal to max_length "
            "(received 11 > 10)",
            str(e.exception),
        )

    # ExpectedParameter

    def test_expected_parameter_repr(self):
        self.assertTrue(
            issubclass(ExpectedParameter, ContractsLanguageDunderMixin),
        )
        self.assertIn("ExpectedParameter", repr(ExpectedParameter))

    def test_expected_parameter_with_string_constraint(self):
        constraint = StringConstraint()
        expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=constraint,
        )
        self.assertEqual("parameter-id", expected_parameter.id)
        self.assertEqual(constraint, expected_parameter.constraint)
        self.assertFalse(expected_parameter.optional)

    def test_expected_parameter_equality(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=constraint,
            
            triggers_pre_parameter_change_hook=False,
        )
        other_constraint = StringConstraint(min_length=1, max_length=10)
        other_expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=other_constraint,
            
            triggers_pre_parameter_change_hook=False,
        )
        self.assertEqual(expected_parameter, other_expected_parameter)

    def test_expected_parameter_unequal_constraint(self):
        constraint = StringConstraint(min_length=1, max_length=10)
        expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=constraint,
        )
        other_constraint = StringConstraint(min_length=1, max_length=42)
        other_expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=other_constraint,
        )
        self.assertNotEqual(expected_parameter, other_expected_parameter)

    def test_expected_parameter_with_account_constraint(self):
        constraint = AccountConstraint()
        expected_parameter = ExpectedParameter(
            id="parameter-id",
            constraint=constraint,
        )
        self.assertEqual(expected_parameter.id, "parameter-id")
        self.assertEqual(expected_parameter.constraint, constraint)

    def test_expected_parameter_raises_with_empty_id(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            ExpectedParameter(id="", constraint=StringConstraint())
        self.assertEqual("ExpectedParameter 'id' must be populated", str(e.exception))

    def test_expected_parameter_with_no_constraint(self):
        expected_parameter = ExpectedParameter(id="parameter-id")
        self.assertEqual("parameter-id", expected_parameter.id)
        self.assertEqual(None, expected_parameter.constraint)

    def test_expected_parameter_raises_with_invalid_constraint(self):
        with self.assertRaises(StrongTypingError) as e:
            ExpectedParameter(id="parameter-id", constraint="not a constraint")
        expected = (
            "Expected Optional[Union[AccountConstraint, DateTimeConstraint, DecimalConstraint, "
            "EnumerationConstraint, StringConstraint]], got 'not a constraint' "
            "of type str"
        )
        self.assertEqual(expected, str(e.exception))

    def test_expected_parameter_with_optional_flag(self):
        expected_parameter = ExpectedParameter(
            id="parameter-id",
            optional=True,
        )
        self.assertEqual("parameter-id", expected_parameter.id)
        self.assertTrue(expected_parameter.optional)

    def test_expected_parameter_raises_with_invalid_optional_flag(self):
        with self.assertRaises(StrongTypingError) as ex:
            ExpectedParameter(id="parameter-id", optional="yes")
        self.assertEqual(
            "Expected Optional[bool] if populated, got 'yes' of type str", str(ex.exception)
        )

    def test_expected_parameter_pre_param_hook_execution_arguments_defaults_correctly(self):
        expected_parameter = ExpectedParameter(id="parameter-id")
        self.assertEqual("parameter-id", expected_parameter.id)
        self.assertIsNone(expected_parameter.triggers_pre_parameter_change_hook)

    def test_expected_parameter_raises_with_invalid_triggers_pre_parameter_change_hook_flag(self):
        with self.assertRaises(StrongTypingError) as ex:
            ExpectedParameter(id="parameter-id", triggers_pre_parameter_change_hook="yes")
        self.assertEqual(
            "Expected Optional[bool] if populated, got 'yes' of type str", str(ex.exception)
        )

    

    # SupervisedHooks

    def test_supervised_hooks(self):
        supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)
        self.assertEqual(supervised_hooks.pre_posting_hook, SupervisionExecutionMode.OVERRIDE)

    def test_supervised_hooks_argument_required(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            SupervisedHooks()

        self.assertEqual(
            str(e.exception),
            "At least one hook supervision must be specified.",
        )

    def test_supervised_hooks_repr(self):
        supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)
        expected = "SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)"
        self.assertEqual(expected, repr(supervised_hooks))

    def test_supervised_hooks_equality(self):
        supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)
        other_supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)
        self.assertEqual(supervised_hooks, other_supervised_hooks)

    def test_supervised_hooks_unequal_pre_posting_hook(self):
        supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.OVERRIDE)
        other_supervised_hooks = SupervisedHooks(pre_posting_hook=SupervisionExecutionMode.INVOKED)
        self.assertNotEqual(supervised_hooks, other_supervised_hooks)

    # Rejection

    def test_rejection(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        self.assertEqual("Rejection", rejection.message)
        self.assertEqual(RejectionReason.INSUFFICIENT_FUNDS, rejection.reason_code)

    def test_rejection_repr(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        expected = "Rejection(message='Rejection', reason_code=RejectionReason.INSUFFICIENT_FUNDS)"
        self.assertEqual(expected, repr(rejection))

    def test_rejection_equality(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS
        )
        self.assertEqual(rejection, other_rejection)

    def test_rejection_unequal_reason_code(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.WRONG_DENOMINATION
        )
        self.assertNotEqual(rejection, other_rejection)

    def test_rejection_with_no_reason_code(self):
        rejection = Rejection(message="Rejection")
        self.assertEqual("Rejection", rejection.message)
        self.assertEqual(None, rejection.reason_code)

    def test_rejection_raises_with_no_message(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            Rejection(message="", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        self.assertEqual("Rejection 'message' must be populated", str(ex.exception))

    def test_rejection_from_proto_skips_validation(self):
        rejection = Rejection(message=True, _from_proto=True)
        self.assertEqual(True, rejection.message)
        self.assertEqual(None, rejection.reason_code)

    # Hook Results

    def test_derived_parameter_result_repr(self):
        result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2019, 12, 12, 13, 20),
                "denomination": "GBP",
                "monthly_repayment": Decimal("500.00"),
                "customer_name": "Paul",
                "tier": UnionItemValue(key="GOLD"),
                "interest_payment_day": OptionalValue(),
                "overdraft_limit": OptionalValue(Decimal("1000.00")),
                "overdraft_fee": OptionalValue(None),
            }
        )
        expected = (
            "DerivedParameterHookResult(parameters_return_value={'interest_account': '1', "
            + "'repayment_date': datetime.datetime(2019, 12, 12, 13, 20), 'denomination': 'GBP', "
            + "'monthly_repayment': Decimal('500.00'), 'customer_name': 'Paul', 'tier': "
            + "UnionItemValue(key='GOLD'), 'interest_payment_day': OptionalValue(value=None), "
            + "'overdraft_limit': OptionalValue(value=Decimal('1000.00')), "
            + "'overdraft_fee': OptionalValue(value=None)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(result))

    def test_derived_parameter_result(self):
        derived_parameters_result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2019, 12, 12, 13, 20),
                "denomination": "GBP",
                "monthly_repayment": Decimal("500.00"),
                "customer_name": "Paul",
                "tier": UnionItemValue(key="GOLD"),
                "interest_payment_day": OptionalValue(),
                "overdraft_limit": OptionalValue(Decimal("1000.00")),
                "overdraft_fee": OptionalValue(None),
            }
        )
        self.assertEqual(9, len(derived_parameters_result.parameters_return_value))

    def test_derived_parameter_result_equality(self):
        derived_parameters_result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2019, 12, 12, 13, 20),
                "denomination": "GBP",
            }
        )
        other_derived_parameters_result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2019, 12, 12, 13, 20),
                "denomination": "GBP",
            }
        )
        self.assertEqual(derived_parameters_result, other_derived_parameters_result)

    def test_derived_parameter_result_unequal_parameters_return_value(self):
        derived_parameters_result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2019, 12, 12, 13, 20),
                "denomination": "GBP",
            }
        )
        other_derived_parameters_result = DerivedParameterHookResult(
            parameters_return_value={
                "interest_account": "1",
                "repayment_date": datetime(2042, 12, 12, 13, 20),
                "denomination": "GBP",
            }
        )
        self.assertNotEqual(derived_parameters_result, other_derived_parameters_result)

    def test_derived_parameter_result_raises_with_invalid_return_value(self):
        with self.assertRaises(StrongTypingError) as ex:
            DerivedParameterHookResult(parameters_return_value=None)
        self.assertEqual(
            "'parameters_return_value' expected dict, got None",
            str(ex.exception),
        )

    def test_deactivation_hook_result_without_directives_and_rejection(self):
        deactivation_hook_result = DeactivationHookResult()
        self.assertEqual([], deactivation_hook_result.account_notification_directives)
        self.assertEqual([], deactivation_hook_result.posting_instructions_directives)
        self.assertIsNone(deactivation_hook_result.rejection)

    def test_deactivation_hook_result_with_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        self.assertEqual(
            account_notification_directives,
            deactivation_hook_result.account_notification_directives,
        )
        self.assertEqual(
            posting_instructions_directives,
            deactivation_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            update_account_event_type_directives,
            deactivation_hook_result.update_account_event_type_directives,
        )

    def test_deactivation_hook_result_with_rejection(self):
        rejection = Rejection(
            message="Cannot close account until loan repaid",
            reason_code=RejectionReason.AGAINST_TNC,
        )
        deactivation_hook_result = DeactivationHookResult(rejection=rejection)
        self.assertEqual(rejection, deactivation_hook_result.rejection)

    def test_deactivation_hook_result_with_rejection_and_directives_errors(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        rejection = Rejection(
            message="Cannot close account until loan repaid",
            reason_code=RejectionReason.AGAINST_TNC,
        )
        with self.assertRaises(InvalidSmartContractError) as ex:
            DeactivationHookResult(
                account_notification_directives=account_notification_directives,
                posting_instructions_directives=posting_instructions_directives,
                update_account_event_type_directives=update_account_event_type_directives,
                rejection=rejection,
            )
        self.assertEqual(
            str(ex.exception),
            "DeactivationHookResult allows the population of directives or rejection, but not both",
        )

    def test_deactivation_hook_result_repr(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        expected = (
            f"DeactivationHookResult(account_notification_directives={repr(account_notification_directives)}, "
            f"posting_instructions_directives={repr(posting_instructions_directives)}, "
            f"update_account_event_type_directives={repr(update_account_event_type_directives)}, "
            f"rejection={repr(deactivation_hook_result.rejection)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(deactivation_hook_result))

    def test_deactivation_hook_result_equality(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )

        self.assertEqual(deactivation_hook_result, other_deactivation_hook_result)

    def test_deactivation_hook_result_unequal_update_account_event_type_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        other_update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2032, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_deactivation_hook_result = DeactivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=other_update_account_event_type_directives,
        )

        self.assertNotEqual(deactivation_hook_result, other_deactivation_hook_result)

    @patch.object(hook_results, "validate_account_directives")
    def test_deactivation_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        DeactivationHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            update_account_event_type_directives=self.test_update_account_event_type_directives,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
            self.test_update_account_event_type_directives,
        )

    def test_post_parameter_change_hook_result_without_directives(self):
        post_parameter_change_hook_result = PostParameterChangeHookResult()
        self.assertEqual([], post_parameter_change_hook_result.account_notification_directives)
        self.assertEqual([], post_parameter_change_hook_result.posting_instructions_directives)
        self.assertEqual([], post_parameter_change_hook_result.update_account_event_type_directives)

    def test_post_parameter_change_hook_result_with_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        self.assertEqual(
            account_notification_directives,
            post_parameter_change_hook_result.account_notification_directives,
        )
        self.assertEqual(
            posting_instructions_directives,
            post_parameter_change_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            update_account_event_type_directives,
            post_parameter_change_hook_result.update_account_event_type_directives,
        )

    @patch.object(hook_results, "validate_account_directives")
    def test_post_parameter_change_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        PostParameterChangeHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            update_account_event_type_directives=self.test_update_account_event_type_directives,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
            self.test_update_account_event_type_directives,
        )

    def test_post_parameter_change_hook_result_repr(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        expected = (
            f"PostParameterChangeHookResult(account_notification_directives={repr(account_notification_directives)}, "
            f"posting_instructions_directives={repr(posting_instructions_directives)}, "
            f"update_account_event_type_directives={repr(update_account_event_type_directives)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(post_parameter_change_hook_result))

    def test_post_parameter_change_hook_result_equality(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )

        self.assertEqual(post_parameter_change_hook_result, other_post_parameter_change_hook_result)

    def test_post_parameter_change_hook_result_unequal_update_account_event_type_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        other_update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2042, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_post_parameter_change_hook_result = PostParameterChangeHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=other_update_account_event_type_directives,
        )

        self.assertNotEqual(
            post_parameter_change_hook_result, other_post_parameter_change_hook_result
        )

    def test_post_posting_hook_result_without_directives(self):
        post_posting_hook_result = PostPostingHookResult()
        self.assertEqual([], post_posting_hook_result.account_notification_directives)
        self.assertEqual([], post_posting_hook_result.posting_instructions_directives)
        self.assertEqual([], post_posting_hook_result.update_account_event_type_directives)

    def test_post_posting_hook_result_with_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        self.assertEqual(
            account_notification_directives,
            post_posting_hook_result.account_notification_directives,
        )
        self.assertEqual(
            posting_instructions_directives,
            post_posting_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            update_account_event_type_directives,
            post_posting_hook_result.update_account_event_type_directives,
        )

    @patch.object(hook_results, "validate_account_directives")
    def test_post_posting_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        PostPostingHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            update_account_event_type_directives=self.test_update_account_event_type_directives,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
            self.test_update_account_event_type_directives,
        )

    def test_post_posting_hook_result_repr(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        expected = (
            f"PostPostingHookResult(account_notification_directives={repr(account_notification_directives)}, "
            f"posting_instructions_directives={repr(posting_instructions_directives)}, "
            f"update_account_event_type_directives={repr(update_account_event_type_directives)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(post_posting_hook_result))

    def test_post_posting_hook_result_equality(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )

        self.assertEqual(
            post_posting_hook_result,
            other_post_posting_hook_result,
        )

    def test_post_posting_hook_result_unequal_update_account_event_type_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        other_update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2042, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_post_posting_hook_result = PostPostingHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=other_update_account_event_type_directives,
        )

        self.assertNotEqual(
            post_posting_hook_result,
            other_post_posting_hook_result,
        )

    def test_post_posting_hook_result_from_proto_skips_validation(self):
        post_posting_hook_result = PostPostingHookResult(
            update_account_event_type_directives=True, _from_proto=True
        )
        self.assertEqual(True, post_posting_hook_result.update_account_event_type_directives)

    def test_pre_parameter_change_hook_result(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_parameter_change_hook_result = PreParameterChangeHookResult(rejection=rejection)
        self.assertEqual(rejection, pre_parameter_change_hook_result.rejection)

    def test_pre_parameter_change_hook_result_repr(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_parameter_change_hook_result = PreParameterChangeHookResult(rejection=rejection)
        expected = (
            "PreParameterChangeHookResult(rejection=Rejection(message='Rejection', "
            + "reason_code=RejectionReason.INSUFFICIENT_FUNDS))"
        )
        self.assertEqual(expected, repr(pre_parameter_change_hook_result))

    def test_pre_parameter_change_hook_result_equality(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_parameter_change_hook_result = PreParameterChangeHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS
        )
        other_pre_parameter_change_hook_result = PreParameterChangeHookResult(
            rejection=other_rejection
        )

        self.assertEqual(pre_parameter_change_hook_result, other_pre_parameter_change_hook_result)

    def test_pre_parameter_change_hook_result_unequal_rejection(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_parameter_change_hook_result = PreParameterChangeHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.WRONG_DENOMINATION
        )
        other_pre_parameter_change_hook_result = PreParameterChangeHookResult(
            rejection=other_rejection
        )

        self.assertNotEqual(
            pre_parameter_change_hook_result, other_pre_parameter_change_hook_result
        )

    def test_pre_parameter_change_hook_result_with_no_rejection(self):
        pre_parameter_change_hook_result = PreParameterChangeHookResult()
        self.assertEqual(None, pre_parameter_change_hook_result.rejection)

    def test_pre_parameter_change_hook_result_raises_with_invalid_rejection_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            PreParameterChangeHookResult(rejection=True)
        self.assertEqual(
            "'rejection' expected Rejection, got 'True' of type bool", str(ex.exception)
        )

    def test_pre_posting_hook_result(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_posting_hook_result = PrePostingHookResult(rejection=rejection)
        self.assertEqual(rejection, pre_posting_hook_result.rejection)

    def test_pre_posting_hook_result_repr(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_posting_hook_result = PrePostingHookResult(rejection=rejection)
        expected = (
            "PrePostingHookResult(rejection=Rejection(message='Rejection', "
            + "reason_code=RejectionReason.INSUFFICIENT_FUNDS))"
        )
        
        self.assertEqual(expected, repr(pre_posting_hook_result))

    def test_pre_posting_hook_result_equality(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_posting_hook_result = PrePostingHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS
        )
        other_pre_posting_hook_result = PrePostingHookResult(rejection=other_rejection)

        self.assertEqual(pre_posting_hook_result, other_pre_posting_hook_result)

    def test_pre_posting_hook_result_unequal_rejection(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        pre_posting_hook_result = PrePostingHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.WRONG_DENOMINATION
        )
        other_pre_posting_hook_result = PrePostingHookResult(rejection=other_rejection)

        self.assertNotEqual(pre_posting_hook_result, other_pre_posting_hook_result)

    def test_pre_posting_hook_result_with_no_rejection(self):
        pre_posting_hook_result = PrePostingHookResult()
        self.assertEqual(None, pre_posting_hook_result.rejection)

    def test_pre_posting_hook_skips_validation(self):
        pre_posting_hook_result = PrePostingHookResult(rejection=True, _from_proto=True)
        self.assertEqual(True, pre_posting_hook_result.rejection)

    

    def test_activation_hook_result_without_directives_or_return_values(self):
        activation_hook_result = ActivationHookResult()
        self.assertEqual([], activation_hook_result.account_notification_directives)
        self.assertEqual([], activation_hook_result.posting_instructions_directives)
        self.assertEqual({}, activation_hook_result.scheduled_events_return_value)

    def test_activation_hook_result_with_directives_and_return_values(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        activation_hook_result = ActivationHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            scheduled_events_return_value=self.test_scheduled_events_return_value,
        )
        self.assertEqual(
            account_notification_directives,
            activation_hook_result.account_notification_directives,
        )
        self.assertEqual(
            posting_instructions_directives,
            activation_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            self.test_scheduled_events_return_value,
            activation_hook_result.scheduled_events_return_value,
        )
        

    @patch.object(hook_results, "validate_account_directives")
    def test_activation_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        ActivationHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            scheduled_events_return_value=self.test_scheduled_events_return_value,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
        )

    

    def test_scheduled_event_hook_result_without_directives(self):
        scheduled_event_hook_result = ScheduledEventHookResult()
        self.assertEqual([], scheduled_event_hook_result.account_notification_directives)
        self.assertEqual([], scheduled_event_hook_result.posting_instructions_directives)
        self.assertEqual([], scheduled_event_hook_result.update_account_event_type_directives)

    def test_scheduled_event_hook_result_with_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        self.assertEqual(
            account_notification_directives,
            scheduled_event_hook_result.account_notification_directives,
        )
        self.assertEqual(
            posting_instructions_directives,
            scheduled_event_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            update_account_event_type_directives,
            scheduled_event_hook_result.update_account_event_type_directives,
        )

    @patch.object(hook_results, "validate_account_directives")
    def test_scheduled_event_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        ScheduledEventHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            update_account_event_type_directives=self.test_update_account_event_type_directives,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
            self.test_update_account_event_type_directives,
            is_scheduled_event_hook=True,
        )

    def test_scheduled_event_hook_result_repr(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        expected = (
            f"ScheduledEventHookResult(account_notification_directives={repr(account_notification_directives)}, "
            f"posting_instructions_directives={repr(posting_instructions_directives)}, "
            f"update_account_event_type_directives={repr(update_account_event_type_directives)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(scheduled_event_hook_result))

    def test_scheduled_event_hook_result_equality(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )

        self.assertEqual(
            scheduled_event_hook_result,
            other_scheduled_event_hook_result,
        )

    def test_scheduled_event_hook_result_unequal_update_account_event_type_directives(self):
        account_notification_directives = [
            AccountNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        posting_instructions_directives = self.test_posting_instructions_directives
        update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        other_update_account_event_type_directives = [
            UpdateAccountEventTypeDirective(
                event_type="event_type_1",
                end_datetime=datetime(2042, 3, 27, tzinfo=ZoneInfo("UTC")),
            )
        ]
        scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=update_account_event_type_directives,
        )
        other_scheduled_event_hook_result = ScheduledEventHookResult(
            account_notification_directives=account_notification_directives,
            posting_instructions_directives=posting_instructions_directives,
            update_account_event_type_directives=other_update_account_event_type_directives,
        )

        self.assertNotEqual(
            scheduled_event_hook_result,
            other_scheduled_event_hook_result,
        )

    def test_scheduled_event_hook_result_from_proto_skips_validation(self):
        scheduled_event_hook_result = ScheduledEventHookResult(
            update_account_event_type_directives=True, _from_proto=True
        )
        self.assertEqual(True, scheduled_event_hook_result.update_account_event_type_directives)

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_account_directives_raises_with_posting_directive_rejection_reasons_for_non_scheduled_hook(
        self,
    ):
        with self.assertRaises(InvalidSmartContractError) as e:
            validate_account_directives(
                account_directives=[],
                posting_directives=[
                    self.test_posting_instructions_directive_with_rejection_reasons
                ],
            )
        self.assertEqual(
            "PostingInstructionsDirective.non_blocking_rejection_reasons can only be "
            "populated in Scheduled Event Hook Results",
            str(e.exception),
        )

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_account_directives_allows_posting_directive_rejection_reasons_for_scheduled_hook(
        self,
    ):
        # No error raised.
        validate_account_directives(
            account_directives=[],
            posting_directives=[self.test_posting_instructions_directive_with_rejection_reasons],
            is_scheduled_event_hook=True,
        )

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_supervisee_directives_raises_with_posting_directive_rejection_reasons_for_non_scheduled_hook(
        self,
    ):
        with self.assertRaises(InvalidSmartContractError) as e:
            validate_supervisee_directives(
                supervisee_account_directives={},
                supervisee_posting_directives={
                    "account_id_1": [
                        self.test_posting_instructions_directive_with_rejection_reasons
                    ]
                },
                supervisee_update_account_directives={},
            )
        self.assertEqual(
            "PostingInstructionsDirective.non_blocking_rejection_reasons can only be "
            "populated in Scheduled Event Hook Results",
            str(e.exception),
        )

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_supervisee_directives_allows_posting_directive_rejection_reasons_for_scheduled_hook(
        self,
    ):
        # No error raised.
        validate_supervisee_directives(
            supervisee_account_directives={},
            supervisee_posting_directives={
                "account_id_1": [self.test_posting_instructions_directive_with_rejection_reasons]
            },
            supervisee_update_account_directives={},
            is_scheduled_event_hook=True,
        )

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_servicing_hook_directives_raises_with_posting_directive_rejection_reasons_for_non_scheduled_hook(
        self,
    ):
        with self.assertRaises(InvalidSmartContractError) as e:
            validate_servicing_hook_directives(
                class_name="Class",
                posting_instructions_directives=[
                    self.test_posting_instructions_directive_with_rejection_reasons
                ],
                servicing_group_notification_directives=[],
                update_servicing_group_event_type_directives=[],
            )
        self.assertEqual(
            "PostingInstructionsDirective.non_blocking_rejection_reasons can only be "
            "populated in Scheduled Event Hook Results",
            str(e.exception),
        )

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_validate_servicing_hook_directives_allows_posting_directive_rejection_reasons_for_scheduled_hook(
        self,
    ):
        # No error raised.
        validate_servicing_hook_directives(
            class_name="Class",
            posting_instructions_directives=[
                self.test_posting_instructions_directive_with_rejection_reasons
            ],
            servicing_group_notification_directives=[],
            update_servicing_group_event_type_directives=[],
            is_scheduled_event_hook=True,
        )

    def test_supervisor_post_posting_hook_result_without_directives(self):
        supervisor_post_posting_hook_result = SupervisorPostPostingHookResult()
        self.assertEqual([], supervisor_post_posting_hook_result.plan_notification_directives)
        self.assertEqual([], supervisor_post_posting_hook_result.update_plan_event_type_directives)

        self.assertEqual(
            {}, supervisor_post_posting_hook_result.supervisee_account_notification_directives
        )
        self.assertEqual(
            {}, supervisor_post_posting_hook_result.supervisee_posting_instructions_directives
        )
        self.assertEqual(
            {}, supervisor_post_posting_hook_result.supervisee_update_account_event_type_directives
        )

    def test_supervisor_post_posting_hook_result_with_directives(self):
        supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=self.test_plan_notification_directives,
            update_plan_event_type_directives=self.test_update_plan_event_type_directives,
            supervisee_account_notification_directives=self.test_supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=self.test_supervisee_posting_instructions_directives,
            supervisee_update_account_event_type_directives=self.test_supervisee_update_account_event_type_directives,
        )
        self.assertEqual(
            self.test_plan_notification_directives,
            supervisor_post_posting_hook_result.plan_notification_directives,
        )
        self.assertEqual(
            self.test_update_plan_event_type_directives,
            supervisor_post_posting_hook_result.update_plan_event_type_directives,
        )

        self.assertEqual(
            self.test_supervisee_account_notification_directives,
            supervisor_post_posting_hook_result.supervisee_account_notification_directives,
        )
        self.assertEqual(
            self.test_supervisee_posting_instructions_directives,
            supervisor_post_posting_hook_result.supervisee_posting_instructions_directives,
        )
        self.assertEqual(
            self.test_supervisee_update_account_event_type_directives,
            supervisor_post_posting_hook_result.supervisee_update_account_event_type_directives,
        )

    @patch.object(hook_results, "validate_supervisee_directives")
    def test_supervisor_post_posting_hook_result_validates_account_directives(
        self, mock_validate_supervisee_directives: Mock
    ):
        SupervisorPostPostingHookResult(
            plan_notification_directives=self.test_plan_notification_directives,
            update_plan_event_type_directives=self.test_update_plan_event_type_directives,
            supervisee_account_notification_directives=self.test_supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=self.test_supervisee_posting_instructions_directives,
            supervisee_update_account_event_type_directives=self.test_supervisee_update_account_event_type_directives,
        )
        mock_validate_supervisee_directives.assert_called_once_with(
            self.test_supervisee_account_notification_directives,
            self.test_supervisee_posting_instructions_directives,
            self.test_supervisee_update_account_event_type_directives,
        )

    def test_supervisor_post_posting_hook_result_repr(self):
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        expected = (
            f"SupervisorPostPostingHookResult(plan_notification_directives={repr(plan_notification_directives)}, "
            f"update_plan_event_type_directives={repr(update_plan_event_type_directives)}, "
            f"supervisee_account_notification_directives={repr(supervisee_account_notification_directives)}, "
            f"supervisee_posting_instructions_directives={repr(supervisee_posting_instructions_directives)}, "
            f"supervisee_update_account_event_type_directives={repr(supervisee_update_account_event_type_directives)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(supervisor_post_posting_hook_result))

    def test_supervisor_post_posting_hook_result_equality(self):
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        other_supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )

        self.assertEqual(
            supervisor_post_posting_hook_result,
            other_supervisor_post_posting_hook_result,
        )

    def test_supervisor_post_posting_hook_result_unequal_supervisee_update_account_event_type_directives(  # noqa: E501
        self,
    ):  # noqa: E501
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }
        other_supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_42",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        other_supervisor_post_posting_hook_result = SupervisorPostPostingHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=other_supervisee_update_account_event_type_directives,  # noqa: E501
        )

        self.assertNotEqual(
            supervisor_post_posting_hook_result,
            other_supervisor_post_posting_hook_result,
        )

    def test_supervisor_pre_posting_hook_result(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(rejection=rejection)
        self.assertEqual(rejection, supervisor_pre_posting_hook_result.rejection)

    def test_supervisor_pre_posting_hook_result_repr(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(rejection=rejection)
        expected = (
            "SupervisorPrePostingHookResult(rejection=Rejection(message='Rejection', "
            + "reason_code=RejectionReason.INSUFFICIENT_FUNDS))"
        )
        self.assertEqual(expected, repr(supervisor_pre_posting_hook_result))

    def test_supervisor_pre_posting_hook_result_equality(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS
        )
        other_supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(
            rejection=other_rejection
        )

        self.assertEqual(
            supervisor_pre_posting_hook_result, other_supervisor_pre_posting_hook_result
        )

    def test_supervisor_pre_posting_hook_result_unequal_rejection(self):
        rejection = Rejection(message="Rejection", reason_code=RejectionReason.INSUFFICIENT_FUNDS)
        supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(rejection=rejection)
        other_rejection = Rejection(
            message="Rejection", reason_code=RejectionReason.CLIENT_CUSTOM_REASON
        )
        other_supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult(
            rejection=other_rejection
        )

        self.assertNotEqual(
            supervisor_pre_posting_hook_result, other_supervisor_pre_posting_hook_result
        )

    def test_supervisor_pre_posting_hook_result_with_no_rejection(self):
        supervisor_pre_posting_hook_result = SupervisorPrePostingHookResult()
        self.assertEqual(None, supervisor_pre_posting_hook_result.rejection)

    def test_supervisor_pre_posting_hook_raises_with_invalid_values(self):
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorPrePostingHookResult(rejection=True)
        self.assertEqual(
            "'rejection' expected Rejection, got 'True' of type bool",
            str(ex.exception),
        )

    def test_supervisor_scheduled_event_hook_result_without_directives(self):
        supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult()
        self.assertEqual([], supervisor_scheduled_event_hook_result.plan_notification_directives)
        self.assertEqual(
            [], supervisor_scheduled_event_hook_result.update_plan_event_type_directives
        )

        self.assertEqual(
            {}, supervisor_scheduled_event_hook_result.supervisee_account_notification_directives
        )
        self.assertEqual(
            {}, supervisor_scheduled_event_hook_result.supervisee_posting_instructions_directives
        )
        self.assertEqual(
            {},
            supervisor_scheduled_event_hook_result.supervisee_update_account_event_type_directives,
        )

    def test_supervisor_scheduled_event_hook_result_with_directives(self):
        supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=self.test_plan_notification_directives,
            update_plan_event_type_directives=self.test_update_plan_event_type_directives,
            supervisee_account_notification_directives=self.test_supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=self.test_supervisee_posting_instructions_directives,
            supervisee_update_account_event_type_directives=self.test_supervisee_update_account_event_type_directives,
        )
        self.assertEqual(
            self.test_plan_notification_directives,
            supervisor_scheduled_event_hook_result.plan_notification_directives,
        )
        self.assertEqual(
            self.test_update_plan_event_type_directives,
            supervisor_scheduled_event_hook_result.update_plan_event_type_directives,
        )

        self.assertEqual(
            self.test_supervisee_account_notification_directives,
            supervisor_scheduled_event_hook_result.supervisee_account_notification_directives,
        )
        self.assertEqual(
            self.test_supervisee_posting_instructions_directives,
            supervisor_scheduled_event_hook_result.supervisee_posting_instructions_directives,
        )
        self.assertEqual(
            self.test_supervisee_update_account_event_type_directives,
            supervisor_scheduled_event_hook_result.supervisee_update_account_event_type_directives,
        )

    @patch.object(hook_results, "validate_supervisee_directives")
    def test_supervisor_scheduled_event_hook_result_validates_account_directives(
        self, mock_validate_supervisee_directives: Mock
    ):
        SupervisorScheduledEventHookResult(
            plan_notification_directives=self.test_plan_notification_directives,
            update_plan_event_type_directives=self.test_update_plan_event_type_directives,
            supervisee_account_notification_directives=self.test_supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=self.test_supervisee_posting_instructions_directives,
            supervisee_update_account_event_type_directives=self.test_supervisee_update_account_event_type_directives,
        )
        mock_validate_supervisee_directives.assert_called_once_with(
            self.test_supervisee_account_notification_directives,
            self.test_supervisee_posting_instructions_directives,
            self.test_supervisee_update_account_event_type_directives,
            is_scheduled_event_hook=True,
        )

    def test_supervisor_scheduled_event_hook_result_repr(self):
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        expected = (
            f"SupervisorScheduledEventHookResult(plan_notification_directives={repr(plan_notification_directives)}, "
            f"update_plan_event_type_directives={repr(update_plan_event_type_directives)}, "
            f"supervisee_account_notification_directives={repr(supervisee_account_notification_directives)}, "
            f"supervisee_posting_instructions_directives={repr(supervisee_posting_instructions_directives)}, "
            f"supervisee_update_account_event_type_directives={repr(supervisee_update_account_event_type_directives)})"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(supervisor_scheduled_event_hook_result))

    def test_supervisor_scheduled_event_hook_result_equality(self):
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        other_supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        self.assertEqual(
            supervisor_scheduled_event_hook_result,
            other_supervisor_scheduled_event_hook_result,
        )

    def test_supervisor_scheduled_event_hook_result_unequal_supervisee_update_account_event_type_directives(  # noqa: E501
        self,
    ):  # noqa: E501
        plan_notification_directives = [
            PlanNotificationDirective(
                notification_type="test_notification_type",
                notification_details={"key1": "value1"},
            )
        ]
        update_plan_event_type_directives = [
            UpdatePlanEventTypeDirective(
                event_type="event_type",
                skip=True,
            )
        ]
        supervisee_account_notification_directives = {
            self.test_account_id: [
                AccountNotificationDirective(
                    notification_type="test_notification_type",
                    notification_details={"key1": "value1"},
                )
            ]
        }
        supervisee_posting_instructions_directives = {
            self.test_account_id: self.test_posting_instructions_directives
        }
        supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }
        other_supervisee_update_account_event_type_directives = {
            self.test_account_id: [
                UpdateAccountEventTypeDirective(
                    event_type="event_type_1",
                    end_datetime=datetime(2042, 3, 27, tzinfo=ZoneInfo("UTC")),
                )
            ]
        }

        supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=supervisee_update_account_event_type_directives,  # noqa: E501
        )
        other_supervisor_scheduled_event_hook_result = SupervisorScheduledEventHookResult(
            plan_notification_directives=plan_notification_directives,
            update_plan_event_type_directives=update_plan_event_type_directives,
            supervisee_account_notification_directives=supervisee_account_notification_directives,
            supervisee_posting_instructions_directives=supervisee_posting_instructions_directives,  # noqa: E501
            supervisee_update_account_event_type_directives=other_supervisee_update_account_event_type_directives,  # noqa: E501
        )
        self.assertNotEqual(
            supervisor_scheduled_event_hook_result,
            other_supervisor_scheduled_event_hook_result,
        )

    def test_conversion_hook_result_without_directives_or_return_values(self):
        conversion_hook_result = ConversionHookResult()
        self.assertEqual([], conversion_hook_result.account_notification_directives)
        self.assertEqual([], conversion_hook_result.posting_instructions_directives)
        self.assertEqual({}, conversion_hook_result.scheduled_events_return_value)
        

    def test_conversion_hook_result_with_directives_and_return_values(self):
        conversion_hook_result = ConversionHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            scheduled_events_return_value=self.test_scheduled_events_return_value,
        )
        self.assertEqual(
            self.test_account_notification_directives,
            conversion_hook_result.account_notification_directives,
        )
        self.assertEqual(
            self.test_posting_instructions_directives,
            conversion_hook_result.posting_instructions_directives,
        )
        self.assertEqual(
            self.test_scheduled_events_return_value,
            conversion_hook_result.scheduled_events_return_value,
        )
        self.assertIsNone(conversion_hook_result.rejection)

    @patch.object(hook_results, "validate_account_directives")
    def test_conversion_hook_result_validates_account_directives(
        self, mock_validate_account_directives: Mock
    ):
        ConversionHookResult(
            account_notification_directives=self.test_account_notification_directives,
            posting_instructions_directives=self.test_posting_instructions_directives,
            scheduled_events_return_value=self.test_scheduled_events_return_value,
        )
        mock_validate_account_directives.assert_called_once_with(
            self.test_account_notification_directives,
            self.test_posting_instructions_directives,
        )

    

    def test_conversion_hook_result_raises_with_invalid_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            ConversionHookResult(account_notification_directives=True)
        expected = (
            "Expected list of AccountNotificationDirective objects for 'account_directives', got "
            "'True'"
        )
        self.assertEqual(expected, str(ex.exception))
        with self.assertRaises(StrongTypingError) as ex:
            ConversionHookResult(posting_instructions_directives=True)
        expected = (
            "Expected list of PostingInstructionsDirective objects for 'posting_directives', got "
            "'True'"
        )
        self.assertEqual(expected, str(ex.exception))
        with self.assertRaises(StrongTypingError) as ex:
            ConversionHookResult(scheduled_events_return_value=True)
        expected = "Expected dict, got 'True' of type bool"
        self.assertEqual(expected, str(ex.exception))

    

    # SmartContractDescriptor

    def test_smart_contract_descriptor(self):
        supervised_smart_contract = SmartContractDescriptor(
            alias="test1",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        self.assertEqual("test1", supervised_smart_contract.alias)

    def test_smart_contract_descriptor_repr(self):
        supervised_smart_contract = SmartContractDescriptor(
            alias="test1",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        expected = (
            "SmartContractDescriptor(alias='test1', "
            + "smart_contract_version_id='test_smart_contract_version_id', "
            + "supervise_post_posting_hook=True, supervised_hooks=None)"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(supervised_smart_contract))

    def test_smart_contract_descriptor_equality(self):
        supervised_smart_contract = SmartContractDescriptor(
            alias="test1",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        other_supervised_smart_contract = SmartContractDescriptor(
            alias="test1",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        self.assertEqual(supervised_smart_contract, other_supervised_smart_contract)

    def test_smart_contract_descriptor_unequal_alias(self):
        supervised_smart_contract = SmartContractDescriptor(
            alias="test1",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        other_supervised_smart_contract = SmartContractDescriptor(
            alias="test2",
            smart_contract_version_id="test_smart_contract_version_id",
            supervise_post_posting_hook=True,
        )
        self.assertNotEqual(supervised_smart_contract, other_supervised_smart_contract)

    def test_smart_contract_descriptor_raises_if_alias_not_populated(self):
        with self.assertRaises(StrongTypingError) as ex:
            SmartContractDescriptor(
                alias=None, smart_contract_version_id="test_smart_contract_version_id"
            )
        self.assertEqual("SmartContractDescriptor 'alias' must be populated", str(ex.exception))

    def test_smart_contract_descriptor_raises_if_smart_contract_version_id_not_populated(self):
        with self.assertRaises(StrongTypingError) as ex:
            SmartContractDescriptor(alias="alias", smart_contract_version_id=None)
        self.assertEqual(
            "SmartContractDescriptor 'smart_contract_version_id' must be populated",
            str(ex.exception),
        )

    def test_smart_contract_descriptor_no_supervised_hooks(self):
        supervised_smart_contract = SmartContractDescriptor(
            alias="test1", smart_contract_version_id="test_smart_contract_version_id"
        )
        self.assertEqual("test1", supervised_smart_contract.alias)
        self.assertIsNone(supervised_smart_contract.supervised_hooks)

    def test_smart_contract_descriptor_raises_with_invalid_supervised_hooks_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            SmartContractDescriptor(
                alias="test1",
                smart_contract_version_id="test_smart_contract_version_id",
                supervised_hooks="foo",
            )
        self.assertEqual(
            "'SmartContractDescriptor.supervised_hooks' expected SupervisedHooks if populated, got "
            "'foo' of type str",
            str(ex.exception),
        )

    # Parameter

    def test_can_construct_parameter(self):
        shape = NumberShape()
        parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=shape,
        )

        self.assertEqual("name", parameter.name)
        self.assertEqual("description", parameter.description)
        self.assertEqual("display_name", parameter.display_name)
        self.assertEqual(ParameterLevel.INSTANCE, parameter.level)
        self.assertEqual(42, parameter.default_value)
        self.assertEqual(shape, parameter.shape)

    def test_parameter_repr(self):
        parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=NumberShape(),
        )
        expected = (
            "Parameter(name='name', shape=NumberShape(min_value=None, max_value=None, step=None), "
            + "level=ParameterLevel.INSTANCE, derived=False, display_name='display_name', "
            + "description='description', default_value=42, update_permission=None)"
        )
        self.assertEqual(expected, repr(parameter))

    def test_parameter_equality(self):
        shape = NumberShape()
        parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=shape,
        )
        other_shape = NumberShape()
        other_parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=other_shape,
        )

        self.assertEqual(parameter, other_parameter)

    def test_parameter_unequal_shape(self):
        shape = NumberShape()
        parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=shape,
        )
        other_shape = NumberShape(min_value=42)
        other_parameter = Parameter(
            name="name",
            description="description",
            display_name="display_name",
            level=ParameterLevel.INSTANCE,
            default_value=42,
            shape=other_shape,
        )

        self.assertNotEqual(parameter, other_parameter)

    # BalancesFilter

    def test_balances_filter_repr(self):
        balances_filter = BalancesFilter(addresses=["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"])
        expected = "BalancesFilter(addresses=['CUSTOM_ADDRESS', 'DEFAULT_ADDRESS'])"
        self.assertEqual(expected, repr(balances_filter))

    def test_balances_filter(self):
        addresses = ["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"]
        balances_filter = BalancesFilter(addresses=addresses)
        self.assertEqual(addresses, balances_filter.addresses)

    def test_balances_filter_equality(self):
        addresses = ["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"]
        balances_filter = BalancesFilter(addresses=addresses)
        other_addresses = ["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"]
        other_balances_filter = BalancesFilter(addresses=other_addresses)

        self.assertEqual(balances_filter, other_balances_filter)

    def test_balances_filter_unequal_addresses(self):
        addresses = ["CUSTOM_ADDRESS", "DEFAULT_ADDRESS"]
        balances_filter = BalancesFilter(addresses=addresses)
        other_addresses = ["CUSTOM_ADDRESS", "DEFAULT_ADDRESS42"]
        other_balances_filter = BalancesFilter(addresses=other_addresses)

        self.assertNotEqual(balances_filter, other_balances_filter)

    def test_balances_filter_raises_with_empty_addresses(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesFilter(addresses=[])
        self.assertEqual(str(e.exception), "'addresses' must be a non empty list, got []")

    def test_balances_filter_raises_with_empty_address_field(self):
        with self.assertRaises(TypeError) as e:
            BalancesFilter()
        self.assertEqual(
            str(e.exception),
            "BalancesFilter.__init__() missing 1 required keyword-only argument: 'addresses'",
        )

    def test_balances_filter_raises_with_addresses_invalid_element_type(self):
        with self.assertRaises(StrongTypingError) as e:
            BalancesFilter(addresses=[None])
        self.assertEqual(str(e.exception), "Expected List[str], got None")

    def test_balances_filter_raises_with_duplicate_addresses(self):
        with self.assertRaises(InvalidSmartContractError) as e:
            BalancesFilter(addresses=["address_1", "address_1"])
        self.assertEqual(
            str(e.exception), "BalancesFilter addresses must not contain any duplicate addresses."
        )

    def test_balances_filter_raises_invalid_argument_type(self):
        with self.assertRaises(StrongTypingError):
            BalancesFilter(addresses=123)

    # PlanNotificationDirective

    def test_plan_notification_directive_equality(self):
        plan_notification_directive = PlanNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value1"},
        )
        other_plan_notification_directive = PlanNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value1"},
        )
        self.assertEqual(plan_notification_directive, other_plan_notification_directive)

    def test_plan_notification_directive_unequal_notification_details(self):
        plan_notification_directive = PlanNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value1"},
        )
        other_plan_notification_directive = PlanNotificationDirective(
            notification_type="test_notification_type",
            notification_details={"key1": "value42"},
        )
        self.assertNotEqual(plan_notification_directive, other_plan_notification_directive)

    # PostingInstructionsDirective

    def test_posting_instructions_directive_repr_inherited_from_mixin(self):
        directive = self.test_posting_instructions_directives[0]
        self.assertTrue(issubclass(PostingInstructionsDirective, ContractsLanguageDunderMixin))
        self.assertIn("PostingInstructionsDirective", repr(directive))

    def test_posting_instructions_directive_equality(self):
        posting_instructions_directive = self.test_posting_instructions_directives[0]
        other_custom_instructions = CustomInstruction(
            postings=[
                Posting(
                    amount=Decimal(1),
                    credit=True,
                    account_id="1",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
                Posting(
                    amount=Decimal(1),
                    credit=False,
                    account_id="2",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
            ]
        )
        other_posting_instructions_directive = PostingInstructionsDirective(
            client_batch_id="international-payment",
            value_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            posting_instructions=[other_custom_instructions],
        )
        self.assertEqual(posting_instructions_directive, other_posting_instructions_directive)

    def test_posting_instructions_directive_unequal_posting_instructions(self):
        posting_instructions_directive = self.test_posting_instructions_directives[0]
        other_custom_instructions = CustomInstruction(
            postings=[
                Posting(
                    amount=Decimal(1),
                    credit=True,
                    account_id="1",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
                Posting(
                    amount=Decimal(1),
                    credit=False,
                    account_id="42",
                    denomination="GBP",
                    account_address=DEFAULT_ADDRESS,
                    asset=DEFAULT_ASSET,
                    phase=Phase.COMMITTED,
                ),
            ]
        )
        other_posting_instructions_directive = PostingInstructionsDirective(
            client_batch_id="international-payment",
            value_datetime=datetime(2022, 3, 27, tzinfo=ZoneInfo("UTC")),
            posting_instructions=[other_custom_instructions],
        )
        self.assertNotEqual(posting_instructions_directive, other_posting_instructions_directive)

    # SmartContractEventType

    def test_smart_contract_event_type_can_be_created(self):
        event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG"])
        self.assertEqual(event_type.name, "name")
        self.assertEqual(event_type.scheduler_tag_ids, ["TAG"])

    def test_smart_contract_event_type_equality(self):
        event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG"])
        other_event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG"])
        self.assertEqual(event_type, other_event_type)

    def test_smart_contract_event_type_unequal_scheduler_tag_ids(self):
        event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG"])
        other_event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG2"])
        self.assertNotEqual(event_type, other_event_type)

    def test_smart_contract_event_type_repr(self):
        event_type = SmartContractEventType(name="name", scheduler_tag_ids=["TAG"])
        expected = "SmartContractEventType(name='name', scheduler_tag_ids=['TAG'])"
        
        self.assertEqual(expected, repr(event_type))

    def test_smart_contract_event_type_when_name_empty(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SmartContractEventType(name="", scheduler_tag_ids=["TAG"])
        expected = (
            "SmartContractEventType 'name' must be populated. Current attributes are "
            + "SmartContractEventType(name='', scheduler_tag_ids=['TAG'])"
        )
        
        self.assertEqual(expected, str(ex.exception))

    def test_smart_contract_event_type_when_scheduler_tag_ids_invalid(self):
        with self.assertRaises(StrongTypingError) as ex:
            SmartContractEventType(name="name", scheduler_tag_ids="invalid")
        self.assertEqual(
            "Expected list of str objects for 'scheduler_tag_ids', got 'invalid'", str(ex.exception)
        )

    

    # SupervisorContractEventType

    def test_supervisor_contract_event_type_can_be_created(self):
        event_type_name = "TEST_EVENT_1"
        scheduler_tag_ids = ["TEST_TAG_1", "TEST_TAG_2"]
        overrides_event_types = [
            ("S1", "TEST_EVENT_2"),
            ("S2", "TEST_EVENT_3"),
        ]

        event_type = SupervisorContractEventType(
            name=event_type_name,
            scheduler_tag_ids=scheduler_tag_ids,
            overrides_event_types=overrides_event_types,
        )

        self.assertEqual(event_type_name, event_type.name)
        self.assertEqual(scheduler_tag_ids, event_type.scheduler_tag_ids)
        self.assertEqual(overrides_event_types, event_type.overrides_event_types)

    def test_supervisor_contract_event_type_equality(self):
        event_type = SupervisorContractEventType(
            name="name",
            scheduler_tag_ids=["TAG"],
            overrides_event_types=[
                ("S1", "TEST_EVENT_2"),
                ("S2", "TEST_EVENT_3"),
            ],
        )
        other_event_type = SupervisorContractEventType(
            name="name",
            scheduler_tag_ids=["TAG"],
            overrides_event_types=[
                ("S1", "TEST_EVENT_2"),
                ("S2", "TEST_EVENT_3"),
            ],
        )

        self.assertEqual(event_type, other_event_type)

    def test_supervisor_contract_event_type_unequal_overrides_event_types(self):
        event_type = SupervisorContractEventType(
            name="name",
            scheduler_tag_ids=["TAG"],
            overrides_event_types=[
                ("S1", "TEST_EVENT_2"),
                ("S2", "TEST_EVENT_3"),
            ],
        )
        other_event_type = SupervisorContractEventType(
            name="name",
            scheduler_tag_ids=["TAG"],
            overrides_event_types=[
                ("S1", "TEST_EVENT_2"),
                ("S2", "TEST_EVENT_42"),
            ],
        )

        self.assertNotEqual(event_type, other_event_type)

    def test_supervisor_contract_event_type_repr(self):
        event_type = SupervisorContractEventType(
            name="TEST_EVENT_1",
            scheduler_tag_ids=["TEST_TAG_1", "TEST_TAG_2"],
            overrides_event_types=[
                ("S1", "TEST_EVENT_2"),
                ("S2", "TEST_EVENT_3"),
            ],
        )

        expected = (
            "SupervisorContractEventType(name='TEST_EVENT_1', "
            + "scheduler_tag_ids=['TEST_TAG_1', 'TEST_TAG_2'], "
            + "overrides_event_types=[('S1', 'TEST_EVENT_2'), ('S2', 'TEST_EVENT_3')])"
        )
        self.maxDiff = None
        self.assertEqual(expected, repr(event_type))

    def test_supervisor_contract_event_type_when_name_empty(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            SupervisorContractEventType(name="", scheduler_tag_ids=["TAG"])
        expected = (
            "SupervisorContractEventType 'name' must be populated. "
            + "Current attributes are SupervisorContractEventType(name='', "
            + "scheduler_tag_ids=['TAG'], overrides_event_types=None)"
        )
        self.maxDiff = None
        self.assertEqual(expected, str(ex.exception))

    def test_supervisor_contract_event_type_when_scheduler_tag_ids_invalid(self):
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorContractEventType(name="name", scheduler_tag_ids="invalid")
        self.assertEqual(
            "Expected list of str objects for 'scheduler_tag_ids', got 'invalid'", str(ex.exception)
        )

    def test_supervisor_contract_event_type_when_scheduler_tag_ids_invalid_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorContractEventType(name="name", scheduler_tag_ids=["TAG", 5])
        self.assertEqual("Expected str, got '5' of type int", str(ex.exception))

    def test_supervisor_contract_event_type_when_overrides_event_types_invalid(self):
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorContractEventType(
                name="name", scheduler_tag_ids=["TAG"], overrides_event_types="invalid"
            )
        self.assertEqual(
            "Expected list of Tuple[str, str] objects for 'overrides_event_types', got "
            "'invalid'",
            str(ex.exception),
        )

    def test_supervisor_contract_event_type_when_overrides_event_types_invalid_type(self):
        with self.assertRaises(StrongTypingError) as ex:
            SupervisorContractEventType(
                name="name",
                scheduler_tag_ids=["TAG"],
                overrides_event_types=[("S1", "TEST_EVENT_1"), 5],
            )
        self.assertEqual("Expected Tuple[str, str], got '5' of type int", str(ex.exception))

    # AddressDetails

    def test_address_details(self):
        address_details = AddressDetails(
            account_address="DEFAULT", description="Some desc", tags=["one", "two"]
        )

        self.assertEqual("DEFAULT", address_details.account_address)
        self.assertEqual("Some desc", address_details.description)
        self.assertEqual(["one", "two"], address_details.tags)

    def test_address_details_repr(self):
        address_details = AddressDetails(
            account_address="DEFAULT", description="Some desc", tags=["one", "two"]
        )
        expected = (
            "AddressDetails(account_address='DEFAULT', "
            + "description='Some desc', tags=['one', 'two'])"
        )
        self.assertEqual(expected, repr(address_details))

    def test_address_details_equality(self):
        default = AddressDetails(
            account_address="DEFAULT", description="Default address", tags=["default"]
        )
        other_default = AddressDetails(
            account_address="DEFAULT", description="Default address", tags=["default"]
        )
        self.assertEqual(default, other_default)

    def test_address_details_unequal_tags(self):
        default = AddressDetails(
            account_address="DEFAULT", description="Default address", tags=["default"]
        )
        other_default = AddressDetails(
            account_address="DEFAULT", description="Default address", tags=["default1"]
        )
        self.assertNotEqual(default, other_default)

    def test_address_details_raises_with_no_address(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            AddressDetails(account_address=None, description="Some desc", tags=["one", "two"])
        self.assertEqual("AddressDetails 'account_address' must be populated", str(ex.exception))

    def test_address_details_raises_with_no_description(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            AddressDetails(account_address="DEFAULT", description=None, tags=["one", "two"])
        self.assertEqual("AddressDetails 'description' must be populated", str(ex.exception))

    def test_address_details_raises_with_no_tags(self):
        with self.assertRaises(InvalidSmartContractError) as ex:
            AddressDetails(account_address="DEFAULT", description="Some desc", tags=None)
        self.assertEqual("AddressDetails 'tags' must be populated", str(ex.exception))

    def test_address_details_raises_with_invalid_tags(self):
        with self.assertRaises(StrongTypingError) as ex:
            AddressDetails(account_address="DEFAULT", description="Some desc", tags=False)
        self.assertEqual("'tags' expected list, got 'False' of type bool", str(ex.exception))

    def test_address_details_skips_validation(self):
        address = AddressDetails(
            account_address="foo", description=None, tags=None, _from_proto=True
        )
        self.assertEqual("foo", address.account_address)

    # Logger

    def test_logger_debug_to_stderr(self):
        logger = Logger.instance()

        with StringIO() as buf:
            with redirect_stderr(buf):
                logger.debug("hello from the tside")

            self.assertEqual("hello from the tside", buf.getvalue().strip())

    def test_logger_raises_on_init(self):
        with self.assertRaises(Exception) as ex:
            Logger()
        self.assertEqual("Logger is a singleton. Use instance() instead.", str(ex.exception))

    # Data Fetcher Decorators
    fetcher_decorator_error = "decorator should not pass anything to hook"

    def test_requires_decorator(self):
        @requires(
            balances="latest",
            calendar=["cal_1"],
            data_scope="all",
            event_type="EVENT",
            flags=True,
            last_execution_datetime=["EVENT"],
            parameters=True,
            postings=True,
        )
        def hook(*args, **kwargs):
            self.assertEqual(args, (), self.fetcher_decorator_error)
            self.assertEqual(kwargs, {}, self.fetcher_decorator_error)

        hook()

    def test_fetch_account_data_decorator(self):
        @fetch_account_data(
            balances=["fetcher_1"],
            event_type="EVENT",
            parameters=["fetcher_2"],
            postings=["fetcher_3"],
            flags=["flags_fetcher_1"],
        )
        def hook(*args, **kwargs):
            self.assertEqual(args, (), self.fetcher_decorator_error)
            self.assertEqual(kwargs, {}, self.fetcher_decorator_error)

        hook()

    # Attribute Hook Result

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_hook_result_with_decimal_value(self):
        attribute_hook_result = AttributeHookResult(attribute_value=Decimal(1000))
        self.assertEqual(attribute_hook_result.attribute_value, Decimal(1000))

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_hook_result_with_datetime_value(self):
        attribute_hook_result = AttributeHookResult(attribute_value=datetime(2024, 1, 1))
        self.assertEqual(attribute_hook_result.attribute_value, datetime(2024, 1, 1))

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_hook_result_with_str_value(self):
        attribute_hook_result = AttributeHookResult(attribute_value="and thanks for all the fish")
        self.assertEqual(attribute_hook_result.attribute_value, "and thanks for all the fish")

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_hook_result_with_none_value(self):
        attribute_hook_result = AttributeHookResult()
        self.assertEqual(attribute_hook_result.attribute_value, None)

    @skip_if_not_enabled(ACCOUNT_ATTRIBUTE_HOOK)
    def test_attribute_hook_result_raises_with_unsupported_value(self):
        with self.assertRaises(StrongTypingError) as ex:
            AttributeHookResult(attribute_value=1)
        self.assertEqual(
            "'attribute_value' expected Union[Decimal, datetime, str] if populated, got '1' of type int",
            str(ex.exception),
        )

    

    @skip_if_not_enabled(EXPECTED_PID_REJECTIONS)
    def test_posting_instruction_rejection_reason_enum(self):
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_PREVENT_DEBITS.value, 1)
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_PREVENT_CREDITS.value, 2)
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_LIMIT_DEBITS.value, 3)
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_LIMIT_CREDITS.value, 4)
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_REVIEW_DEBITS.value, 5)
        self.assertEqual(PostingInstructionRejectionReason.RESTRICTION_REVIEW_CREDITS.value, 6)
        self.assertEqual(PostingInstructionRejectionReason.INSUFFICIENT_FUNDS.value, 7)
        self.assertEqual(PostingInstructionRejectionReason.AGAINST_TERMS_AND_CONDITIONS.value, 8)
        self.assertEqual(PostingInstructionRejectionReason.CLIENT_CUSTOM_REASON.value, 9)
        self.assertEqual(PostingInstructionRejectionReason.ACCOUNT_STATUS_INVALID.value, 10)
        self.assertEqual(PostingInstructionRejectionReason.WRONG_DENOMINATION.value, 11)
