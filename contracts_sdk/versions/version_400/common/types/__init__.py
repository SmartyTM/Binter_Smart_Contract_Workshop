from typing import Any

from .....utils.feature_flags import (
    is_fflag_enabled,
    ACCOUNTS_V2,
    CONTRACTS_SIMULATION_LOGGING,
    CONTRACTS_BOOKING_PERIODS,
    FLAGS_SERVICE_V2,
    ACCOUNT_ATTRIBUTE_HOOK,
    
    
    EXPECTED_PID_REJECTIONS,
    
)


from .balances import (  # noqa: F401
    AddressDetails,
    Balance,
    BalanceCoordinate,
    BalanceDefaultDict,
    BalancesObservation,
)
from .calendars import CalendarEvent, CalendarEvents  # noqa: F401
from .constants import (  # noqa: F401
    defaultAsset,
    transaction_reference_field_name,
    defaultAddress,
    DEFAULT_ASSET,
    TRANSACTION_REFERENCE_FIELD_NAME,
    DEFAULT_ADDRESS,
)



from .attributes import Attribute
from .attribute_data_types import AttributeDecimalType, AttributeDateTimeType, AttributeStringType

from .enums import (  # noqa: F401
    
    
    DateTimePrecision,
    
    Phase,
    PostingInstructionRejectionReason,
    PostingInstructionType,
    RejectionReason,
    SupervisionExecutionMode,
    Timeline,
    Tside,
)
from .event_types import (  # noqa: F401
    EventTypesGroup,
    ScheduledEvent,
    ScheduleExpression,
    ScheduleSkip,
    SmartContractEventType,
    SupervisorContractEventType,
    
)

from .expected_parameters import (  # noqa: F401
    AccountConstraint,
    DateTimeConstraint,
    DecimalConstraint,
    EnumerationConstraint,
    ExpectedParameter,
    StringConstraint,
)

from .fetchers import (  # noqa: F401
    BalancesIntervalFetcher,
    BalancesObservationFetcher,
    fetch_account_data,
    fetch_account_data_with_flags_docstring,
    
    FlagsIntervalFetcher,
    FlagsObservationFetcher,
    IntervalFetcher,
    ParametersIntervalFetcher,
    ParametersObservationFetcher,
    PostingsIntervalFetcher,
    requires,
)

from .flags import FlagsObservation

from .filters import (  # noqa: F401
    BalancesFilter,
    FlagsFilter,
    ParametersFilter,
    
)

from .hook_arguments import (  # noqa: F401
    ActivationHookArguments,
    AttributeHookArguments,
    ConversionHookArguments,
    DeactivationHookArguments,
    DerivedParameterHookArguments,
    PostParameterChangeHookArguments,
    PostPostingHookArguments,
    PreParameterChangeHookArguments,
    PrePostingHookArguments,
    
    ScheduledEventHookArguments,
    
    SupervisorActivationHookArguments,
    SupervisorConversionHookArguments,
    SupervisorPostPostingHookArguments,
    SupervisorPrePostingHookArguments,
    SupervisorScheduledEventHookArguments,
)
from .hook_results import (  # noqa: F401
    DeactivationHookResult,
    DerivedParameterHookResult,
    PreParameterChangeHookResult,
    ActivationHookResult,
    PostParameterChangeHookResult,
    
    PostPostingHookResult,
    PrePostingHookResult,
    
    ScheduledEventHookResult,
    SupervisorActivationHookResult,
    SupervisorConversionHookResult,
    SupervisorPostPostingHookResult,
    SupervisorPrePostingHookResult,
    SupervisorScheduledEventHookResult,
    ConversionHookResult,
    AttributeHookResult,
    
)
from .log import Logger  # noqa: F401
from .account_notification_directive import AccountNotificationDirective  # noqa: F401
from .parameters import (  # noqa: F401
    AccountIdShape,
    DateShape,
    DenominationShape,
    ParameterLevel,
    NumberShape,
    OptionalShape,
    OptionalValue,
    Parameter,
    StringShape,
    UnionItem,
    UnionItemValue,
    UnionShape,
    ParameterUpdatePermission,
)

from .parameter_values import (  # noqa: F401
    ParametersObservation,
)

from .plan_notification_directive import PlanNotificationDirective  # noqa: F401
from .posting_instructions_directive import PostingInstructionsDirective  # noqa: F401
from .postings import (  # noqa: F401
    AdjustmentAmount,
    AuthorisationAdjustment,
    
    ClientTransaction,
    ClientTransactionEffects,
    CustomInstruction,
    
    InboundAuthorisation,
    InboundHardSettlement,
    OutboundAuthorisation,
    OutboundHardSettlement,
    Posting,
    Release,
    Settlement,
    TransactionCode,
    Transfer,
)
from .rejection import Rejection  # noqa: F401
from .schedules import EndOfMonthSchedule, ScheduleFailover  # noqa: F401


from .supervision import SmartContractDescriptor, SupervisedHooks  # noqa: F401
from .time_operations import (  # noqa: F401
    DefinedDateTime,
    Next,
    Override,
    Previous,
    RelativeDateTime,
    Shift,
)
from .timeseries import (  # noqa: F401
    
    TimeseriesItem,
    BalanceTimeseries,
    FlagTimeseries,
    FlagValueTimeseries,
    ParameterTimeseries,
    ParameterValueTimeseries,
)
from .update_account_event_type_directive import UpdateAccountEventTypeDirective  # noqa: F401
from .update_plan_event_type_directive import UpdatePlanEventTypeDirective  # noqa: F401




def common_types_registry() -> dict[str, Any]:
    registry = {
        "AccountIdShape": AccountIdShape,  # noqa: F405
        "AddressDetails": AddressDetails,  # noqa: F405
        "AdjustmentAmount": AdjustmentAmount,
        "AuthorisationAdjustment": AuthorisationAdjustment,
        "Balance": Balance,  # noqa: F405
        "BalanceCoordinate": BalanceCoordinate,  # noqa: F405
        "BalanceDefaultDict": BalanceDefaultDict,  # noqa: F405
        "BalancesFilter": BalancesFilter,  # noqa: F405
        "BalancesIntervalFetcher": BalancesIntervalFetcher,  # noqa: F405
        "BalancesObservation": BalancesObservation,  # noqa: F405
        "BalancesObservationFetcher": BalancesObservationFetcher,  # noqa: F405
        "BalanceTimeseries": BalanceTimeseries,  # noqa: F405
        "CalendarEvent": CalendarEvent,  # noqa: F405
        "CalendarEvents": CalendarEvents,  # noqa: F405
        "ClientTransaction": ClientTransaction,  # noqa: F405
        "ClientTransactionEffects": ClientTransactionEffects,  # noqa: F405
        "DeactivationHookArguments": DeactivationHookArguments,
        "DeactivationHookResult": DeactivationHookResult,
        "CustomInstruction": CustomInstruction,
        "DateShape": DateShape,  # noqa: F405
        "DEFAULT_ADDRESS": defaultAddress,  # noqa: F405
        "DEFAULT_ASSET": defaultAsset,  # noqa: F405
        "DefinedDateTime": DefinedDateTime,
        "DenominationShape": DenominationShape,  # noqa: F405
        "DerivedParameterHookArguments": DerivedParameterHookArguments,
        "DerivedParameterHookResult": DerivedParameterHookResult,
        "EndOfMonthSchedule": EndOfMonthSchedule,  # noqa: F405
        "EventTypesGroup": EventTypesGroup,
        "fetch_account_data": fetch_account_data,
        "FlagTimeseries": FlagTimeseries,  # noqa: F405
        "AccountNotificationDirective": AccountNotificationDirective,  # noqa: F405
        "InboundAuthorisation": InboundAuthorisation,
        "InboundHardSettlement": InboundHardSettlement,
        "ParameterLevel": ParameterLevel,
        "Next": Next,  # noqa: F405
        "NumberShape": NumberShape,  # noqa: F405
        "OptionalShape": OptionalShape,  # noqa: F405
        "OptionalValue": OptionalValue,  # noqa: F405
        "OutboundAuthorisation": OutboundAuthorisation,
        "OutboundHardSettlement": OutboundHardSettlement,
        "Override": Override,  # noqa: F405
        "Parameter": Parameter,  # noqa: F405
        "ParameterTimeseries": ParameterTimeseries,  # noqa: F405
        "Phase": Phase,
        "PlanNotificationDirective": PlanNotificationDirective,
        "ActivationHookArguments": ActivationHookArguments,
        "ActivationHookResult": ActivationHookResult,
        "Posting": Posting,  # noqa: F405
        "PostingInstructionsDirective": PostingInstructionsDirective,  # noqa: F405
        "PostingInstructionType": PostingInstructionType,  # noqa: F405
        "PostingsIntervalFetcher": PostingsIntervalFetcher,  # noqa: F405
        "PostParameterChangeHookArguments": PostParameterChangeHookArguments,
        "PostParameterChangeHookResult": PostParameterChangeHookResult,
        "PostPostingHookArguments": PostPostingHookArguments,
        "PostPostingHookResult": PostPostingHookResult,
        "PrePostingHookResult": PrePostingHookResult,
        "PreParameterChangeHookArguments": PreParameterChangeHookArguments,
        "PreParameterChangeHookResult": PreParameterChangeHookResult,
        "PrePostingHookArguments": PrePostingHookArguments,
        "Previous": Previous,  # noqa: F405
        "Rejection": Rejection,
        "RejectionReason": RejectionReason,
        "RelativeDateTime": RelativeDateTime,  # noqa: F405
        "Release": Release,
        "requires": requires,
        "ScheduleExpression": ScheduleExpression,
        "ScheduledEventHookArguments": ScheduledEventHookArguments,
        "ScheduledEventHookResult": ScheduledEventHookResult,
        "ScheduledEvent": ScheduledEvent,
        "ScheduleFailover": ScheduleFailover,
        "ScheduleSkip": ScheduleSkip,
        "Settlement": Settlement,
        "Shift": Shift,  # noqa: F405
        "SmartContractDescriptor": SmartContractDescriptor,  # noqa: F405
        "SmartContractEventType": SmartContractEventType,
        "StringShape": StringShape,  # noqa: F405
        "SupervisedHooks": SupervisedHooks,
        "SupervisionExecutionMode": SupervisionExecutionMode,
        "SupervisorActivationHookArguments": SupervisorActivationHookArguments,
        "SupervisorActivationHookResult": SupervisorActivationHookResult,
        "SupervisorContractEventType": SupervisorContractEventType,
        "SupervisorConversionHookArguments": SupervisorConversionHookArguments,
        "SupervisorConversionHookResult": SupervisorConversionHookResult,
        "SupervisorPostPostingHookArguments": SupervisorPostPostingHookArguments,
        "SupervisorPostPostingHookResult": SupervisorPostPostingHookResult,
        "SupervisorPrePostingHookArguments": SupervisorPrePostingHookArguments,
        "SupervisorPrePostingHookResult": SupervisorPrePostingHookResult,
        "SupervisorScheduledEventHookArguments": SupervisorScheduledEventHookArguments,
        "SupervisorScheduledEventHookResult": SupervisorScheduledEventHookResult,
        "Timeline": Timeline,
        "TimeseriesItem": TimeseriesItem,  # noqa: F405
        "TransactionCode": TransactionCode,  # noqa: F405
        "TRANSACTION_REFERENCE_FIELD_NAME": transaction_reference_field_name,  # noqa: F405
        "Transfer": Transfer,
        "Tside": Tside,
        "UnionItem": UnionItem,  # noqa: F405
        "UnionItemValue": UnionItemValue,  # noqa: F405
        "UnionShape": UnionShape,  # noqa: F405
        "UpdateAccountEventTypeDirective": UpdateAccountEventTypeDirective,
        "ParameterUpdatePermission": ParameterUpdatePermission,
        "UpdatePlanEventTypeDirective": UpdatePlanEventTypeDirective,
        "ConversionHookArguments": ConversionHookArguments,
        "ConversionHookResult": ConversionHookResult,
    }
    if is_fflag_enabled(ACCOUNTS_V2):
        registry["AccountConstraint"] = AccountConstraint
        registry["DateTimeConstraint"] = DateTimeConstraint
        registry["DateTimePrecision"] = DateTimePrecision
        registry["DecimalConstraint"] = DecimalConstraint
        registry["EnumerationConstraint"] = EnumerationConstraint
        registry["ExpectedParameter"] = ExpectedParameter
        registry["ParametersFilter"] = ParametersFilter  # noqa: F405
        registry["ParametersIntervalFetcher"] = ParametersIntervalFetcher  # noqa: F405
        registry["ParametersObservationFetcher"] = ParametersObservationFetcher  # noqa: F405
        registry["ParametersObservation"] = ParametersObservation
        registry["ParameterValueTimeseries"] = ParameterValueTimeseries
        registry["StringConstraint"] = StringConstraint

    if is_fflag_enabled(CONTRACTS_SIMULATION_LOGGING):
        registry["Logger"] = Logger  # noqa: F405

    if is_fflag_enabled(CONTRACTS_BOOKING_PERIODS):
        registry["BookingPeriod"] = BookingPeriod

    if is_fflag_enabled(FLAGS_SERVICE_V2):
        registry["FlagsFilter"] = FlagsFilter
        registry["FlagsIntervalFetcher"] = FlagsIntervalFetcher
        registry["FlagsObservation"] = FlagsObservation
        registry["FlagsObservationFetcher"] = FlagsObservationFetcher
        registry["FlagValueTimeseries"] = FlagValueTimeseries
        registry["fetch_account_data"].docstring = fetch_account_data_with_flags_docstring

    if not is_fflag_enabled(FLAGS_SERVICE_V2):
        for index, smart_contract_arg in enumerate(
            registry["fetch_account_data"].smart_contract_args
        ):
            if smart_contract_arg.name == "flags":
                del registry["fetch_account_data"].smart_contract_args[index]
                break

    if is_fflag_enabled(ACCOUNT_ATTRIBUTE_HOOK):
        registry["Attribute"] = Attribute
        registry["AttributeHookArguments"] = AttributeHookArguments
        registry["AttributeHookResult"] = AttributeHookResult
        registry["AttributeDecimalType"] = AttributeDecimalType
        registry["AttributeDateTimeType"] = AttributeDateTimeType
        registry["AttributeStringType"] = AttributeStringType

    

    

    

    if is_fflag_enabled(EXPECTED_PID_REJECTIONS):
        registry["PostingInstructionRejectionReason"] = PostingInstructionRejectionReason

    

    return registry
