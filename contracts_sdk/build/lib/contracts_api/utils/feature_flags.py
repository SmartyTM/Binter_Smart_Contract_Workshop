from functools import wraps
import unittest
from unittest.mock import patch
from . import feature_flags_config

# A list of feature flags used in the Contracts Language library.
MOVE_SCX_PARSE_ENDPOINT_TO_CP = "TM_70887_MOVE_SCX_PARSE_ENDPOINT_TO_CP"
MOVE_CX_PARSE_ENDPOINT_TO_CP = "TM_71209_MOVE_CX_PARSE_ENDPOINT_TO_CP"
ACCOUNTS_V2 = "CPP_1430_ACCOUNTS_V2"
CONTRACTS_SIMULATION_LOGGING = "TM_71633_CONTRACTS_SIMULATION_LOGGING"
CONTRACTS_SIMULATION_LOGGING_SUPERVISORS_AND_MODULES = (
    "TM_78716_CONTRACTS_SIMULATION_LOGGING_SUPERVISORS_AND_MODULES"
)
REJECTION_FROM_ACTIVATION_CONVERSION_HOOKS = "TM_78259_REJECTION_FROM_ACTIVATION_CONVERSION_HOOKS"
CONTRACTS_BOOKING_PERIODS = "TM_76761_CONTRACTS_BOOKING_PERIODS"
PROCESSING_GROUPS = "TM_71957_PROCESSING_GROUPS"
FLAGS_SERVICE_V2 = "TM_85182_FLAGS_SERVICE_V2"
ACCOUNT_ATTRIBUTE_HOOK = "IMP_1017_ACCOUNT_ATTRIBUTE_HOOK"
ADJUSTMENTS = "TM_88424_ADJUSTMENTS"
SERVICING_GROUPS = "IMP_681_SERVICING_GROUPS"
MULTIPLE_PROCESSING_GROUPS = "IMP_4_MULTIPLE_PROCESSING_GROUPS"
POST_PARAMETER_IMPROVEMENTS = "IMP_2_POST_PARAMETER_IMPROVEMENTS"
EXPECTED_PID_REJECTIONS = "IMP_50_EXPECTED_POSTING_INSTRUCTION_DIRECTIVE_REJECTIONS"
ENRICH_POSTING_INSTRUCTIONS = "IMP_1154_ENRICH_POSTING_INSTRUCTIONS"
CONTRACTS_SIMULATION_DF_TRACING = "TM_97355_DATA_FETCHER_SIMULATION_TRACING"
POSTINGS_TARGET_ADDRESS = "IMP_1090_POSTINGS_TARGET_ADDRESS"


CONTRACT_LANGUAGE_FFLAGS = [
    MOVE_SCX_PARSE_ENDPOINT_TO_CP,
    MOVE_CX_PARSE_ENDPOINT_TO_CP,
    ACCOUNTS_V2,
    CONTRACTS_SIMULATION_LOGGING,
    CONTRACTS_SIMULATION_LOGGING_SUPERVISORS_AND_MODULES,
    REJECTION_FROM_ACTIVATION_CONVERSION_HOOKS,
    CONTRACTS_BOOKING_PERIODS,
    PROCESSING_GROUPS,
    FLAGS_SERVICE_V2,
    ACCOUNT_ATTRIBUTE_HOOK,
    ADJUSTMENTS,
    SERVICING_GROUPS,
    MULTIPLE_PROCESSING_GROUPS,
    POST_PARAMETER_IMPROVEMENTS,
    EXPECTED_PID_REJECTIONS,
    ENRICH_POSTING_INSTRUCTIONS,
    CONTRACTS_SIMULATION_DF_TRACING,
    POSTINGS_TARGET_ADDRESS,
]


def is_fflag_enabled(feature_flag: str) -> bool:
    """
    Checks if a feature flag is enabled within the CONTRACT_FFLAGS_CONFIG.
    Returns a boolean to indicate if the checked flag is enabled.
    """
    return feature_flags_config.CONTRACT_FFLAGS_CONFIG.get(feature_flag, False)


def skip_if_not_enabled(feature_flag: str):
    """
    Decorator that skips a given test if the passed feature flag is not enabled
    within the CONTRACT_FFLAGS_CONFIG.
    """

    def skip_wrapper(test):
        @wraps(test)
        def wrapped_test(test_instance, *args, **kwargs):
            if not is_fflag_enabled(feature_flag):
                raise unittest.SkipTest(f"Feature flag {feature_flag} not enabled in environment.")
            else:
                return test(test_instance, *args, **kwargs)

        return wrapped_test

    return skip_wrapper


def disable_fflags(feature_flags: list[str]):
    """
    Decorator to be used on tests that disables the given fflags for the duration of that test,
    by mocking the value as False within the CONTRACT_FFLAGS_CONFIG.
    """

    if not (
        isinstance(feature_flags, list) and all(isinstance(item, str) for item in feature_flags)
    ):
        raise TypeError("Please provide a list of feature flag names")

    def disable_wrapper(test):
        @wraps(test)
        def wrapped_test(test_instance, *args, **kwargs):
            with patch.dict(
                feature_flags_config.CONTRACT_FFLAGS_CONFIG,
                values={f: False for f in feature_flags},
            ):
                return test(test_instance, *args, **kwargs)

        return wrapped_test

    return disable_wrapper


def get_enabled_fflags() -> str:
    """
    Returns a comma concatenated string of the currently enabled feature flags.
    """
    return ",".join(
        sorted([k for k, v in feature_flags_config.CONTRACT_FFLAGS_CONFIG.items() if v])
    )
