from functools import lru_cache, wraps
from typing import Optional, Union

from .enums import (
    DefinedDateTime,
    
)
from .time_operations import RelativeDateTime

from ...common.docs import _common_docs_path
from .....utils import exceptions, symbols, types_utils
from .....utils.feature_flags import (
    
    is_fflag_enabled,
)
from .filters import (
    
    BalancesFilter,
    FlagsFilter,
    ParametersFilter,
)




def _requires(
    *,
    balances: Optional[str] = None,
    calendar: Optional[list[str]] = None,
    data_scope: Optional[str] = None,
    event_type: Optional[str] = None,
    flags: Optional[bool] = None,
    last_execution_datetime: Optional[list[str]] = None,
    parameters: Optional[bool] = None,
    postings: Optional[bool] = None,
    supervisee_hook_directives: Optional[str] = None,
):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator

    return wrapper


requires = types_utils.DecoratorSpec(
    name="requires",
    object=_requires,
    docstring="`@requires(*, balances, calendar, data_scope, event_type, flags, "
    "last_execution_datetime, parameters, postings, supervisee_hook_directives)`\n\n"
    "See full requirements reference for [Smart Contracts](/reference/contracts/contracts_api_4xx/"
    "smart_contracts_api_reference4xx/hook_requirements) and [Supervisors](/reference/contracts/"
    "contracts_api_4xx/supervisor_contracts_api_reference4xx/hook_requirements)\n\n"
    "__Note:__ the `scheduled_event_hook` can be decorated with multiple `@requires` decorators to "
    "define requirements per event_type",
    args=[
        types_utils.ValueSpec(
            name="balances",
            type="str",
            docstring="""
                A [Range Specifier](/reference/contracts/contracts_api_4xx/concepts/#requirements-range_specifiers)
                for example "1 day live"
            """,  # noqa: E501,
        ),
        types_utils.ValueSpec(
            name="calendar",
            type="List[str]",
            docstring="A list of Calendar IDs of the required Calendar Events",
        ),
        types_utils.ValueSpec(
            name="data_scope",
            type="str",
            docstring="See [supervisor data scope](../../supervisor_contracts_api_reference4xx/"
            "hook_requirements/#data_scope)<br>  \n(**Supervisor Only**)",
        ),
        types_utils.ValueSpec(
            name="event_type",
            type="str",
            docstring="The defined [metadata event_type](/reference/contracts/contracts_api_4xx/"
            "smart_contracts_api_reference4xx/metadata/#event_types) that the requirements will "
            'fetch, for example: `@requires(event_type="ACCRUE_INTEREST", ...)`\n(only applies '
            "to `scheduled_event_hook`)",
        ),
        types_utils.ValueSpec(
            name="flags",
            type="bool",
            docstring="Defaults to False",
        ),
        types_utils.ValueSpec(
            name="last_execution_datetime",
            type="List[str]",
            docstring="A list of [`event_types`](/reference/contracts/contracts_api_4xx/"
            "smart_contracts_api_reference4xx/metadata/#event_types) to retrieve last execution "
            "datetimes for",
        ),
        types_utils.ValueSpec(
            name="parameters",
            type="bool",
            docstring="Defaults to False",
        ),
        types_utils.ValueSpec(
            name="postings",
            type="str",
            docstring="""
                A [Range Specifier](/reference/contracts/contracts_api_4xx/concepts/#requirements-range_specifiers)
                for example "1 day live"
            """,  # noqa: E501
        ),
        types_utils.ValueSpec(
            name="supervisee_hook_directives",
            type="str",
            docstring="""
                One of `none`, `all` or `invoked` that defaults to `none`
                <br>  \n(**Supervisor Only**)
            """,
        ),
    ],
)


def _fetch_account_data(
    *,
    balances: Optional[Union[list[str], dict[str, list[str]]]] = None,
    event_type: Optional[str] = None,
    parameters: Optional[list[str]] = None,
    postings: Optional[list[str]] = None,
    flags: Optional[list[str]] = None,
    
):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator

    return wrapper





# This is used to override the docstring in the fetch_account_data in the types
# registry (behind a fflag).
fetch_account_data_with_flags_docstring = (
    "`@fetch_account_data(*, balances, event_type, flags, parameters, postings)`"
    "\n\nSee full account fetcher requirements for [Smart Contracts]"
    "(/reference/contracts/contracts_api_4xx/smart_contracts_api_reference4xx/account_fetcher_requirements)"  # noqa: E501
    " and "
    "[Supervisors](/reference/contracts/contracts_api_4xx/supervisor_contracts_api_reference4xx/account_fetcher_requirements)"  # noqa: E501
)
fetch_account_data = types_utils.DecoratorSpec(
    name="fetch_account_data",
    object=_fetch_account_data,
    docstring="`@fetch_account_data(*, balances, event_type, parameters, postings)`"
    "\n\nSee full account fetcher requirements for [Smart Contracts]"
    "(/reference/contracts/contracts_api_4xx/smart_contracts_api_reference4xx/account_fetcher_requirements)"  # noqa: E501
    " and "
    "[Supervisors](/reference/contracts/contracts_api_4xx/supervisor_contracts_api_reference4xx/account_fetcher_requirements)",  # noqa: E501
    smart_contract_args=[
        types_utils.ValueSpec(
            name="balances",
            type="List[str]",
            docstring="A list of [BalancesIntervalFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#BalancesIntervalFetcher) or "
            "[BalancesObservationFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#BalancesObservationFetcher) "
            "Fetcher IDs",
        ),
        types_utils.ValueSpec(
            name="event_type",
            type="str",
            docstring="The defined [metadata event_type](/reference/contracts/contracts_api_4xx/"
            "smart_contracts_api_reference4xx/metadata/#event_types) that the data will be "
            'fetched for, for example: `@fetch_account_data(event_type="ACCRUE_INTEREST", ...)`\n(only applies '
            "to `scheduled_event_hook`)",
        ),
        types_utils.ValueSpec(
            name="flags",
            type="List[str]",
            docstring=f"A list of [FlagsIntervalFetcher]({_common_docs_path}classes/#FlagsIntervalFetcher) and "  # noqa: F541
            f"[FlagsObservationFetcher]({_common_docs_path}classes/#FlagsObservationFetcher) Fetcher IDs",  # noqa: F541
        ),
        types_utils.ValueSpec(
            name="parameters",
            type="List[str]",
            docstring="A list of [ParametersIntervalFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#ParametersIntervalFetcher) or "
            "[ParametersObservationFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#ParametersObservationFetcher) "
            "Fetcher IDs",
        ),
        types_utils.ValueSpec(
            name="postings",
            type="List[str]",
            docstring="A list of [PostingsIntervalFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#PostingsIntervalFetcher) Fetcher IDs",
        ),
    ],
    supervisor_args=[
        types_utils.ValueSpec(
            name="balances",
            type="Dict[str, List[str]]",
            docstring="A dictionary where the key is Supervisee [SmartContractDescriptor]"
            f"({_common_docs_path}"
            "classes/#SmartContractDescriptor) alias and value is a list of "
            "[BalancesIntervalFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#BalancesIntervalFetcher) or "
            "[BalancesObservationFetcher](/reference/contracts/contracts_api_4xx/"
            "common_types_4xx/classes/#BalancesObservationFetcher) "
            "Fetcher IDs.<br>  \n*Note: Currently only available in `pre_posting_hook`*",
        ),
    ],
    
)




class IntervalFetcher(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        *,
        fetcher_id: str,
        start: Union[RelativeDateTime, DefinedDateTime],
        end: Optional[Union[RelativeDateTime, DefinedDateTime]] = DefinedDateTime.LIVE,
    ):
        self.fetcher_id = fetcher_id
        self.start = start
        self.end = end
        self._validate_attributes()

    def _validate_attributes(self):
        class_name = self.__class__.__name__

        types_utils.validate_type(
            self.fetcher_id,
            str,
            hint="str",
            check_empty=True,
            prefix=f"{class_name}.fetcher_id",
        )

        types_utils.validate_type(
            self.start,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[RelativeDateTime, DefinedDateTime]",
            prefix=f"{class_name}.start",
        )
        if (
            isinstance(self.start, RelativeDateTime)
            and self.start.origin != DefinedDateTime.EFFECTIVE_DATETIME
        ):
            raise exceptions.InvalidSmartContractError(
                f"{class_name} 'start' origin value must be set to "
                "'DefinedDateTime.EFFECTIVE_DATETIME'"
            )

        if self.start == DefinedDateTime.LIVE:
            raise exceptions.InvalidSmartContractError(
                f"{class_name} 'start' cannot be set to 'DefinedDateTime.LIVE'"
            )

        if self.start == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                f"{class_name} 'start' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

        types_utils.validate_type(
            self.end,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[RelativeDateTime, DefinedDateTime]",
            is_optional=True,
            prefix=f"{class_name}.end",
        )
        if self.end == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                f"{class_name} 'end' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="fetcher_id",
                type="str",
                docstring=f"""
                    The ID for this fetcher. This can be used in the
                    [@fetch_account_data decorator]({_common_docs_path}decorators/#fetch_account_data)
                    to request the data window defined in this fetcher.
                """,  # noqa: E501
            ),
            types_utils.ValueSpec(
                name="start",
                type="Union[RelativeDateTime, DefinedDateTime]",
                docstring=f"""
                    The start time of the interval window. This can either be a
                    [RelativeDateTime]({_common_docs_path}classes/#RelativeDateTime)
                    or a [DefinedDateTime]({_common_docs_path}enums/#DefinedDateTime).
                    The values `DefinedDateTime.INTERVAL_START` and `DefinedDateTime.LIVE` are
                    **not** allowed. If the value is of type `RelativeDateTime`, its origin must
                    be set to `DefinedDateTime.EFFECTIVE_DATETIME`.
                """,  # noqa E501
            ),
            types_utils.ValueSpec(
                name="end",
                type="Optional[Union[RelativeDateTime, DefinedDateTime]]",
                docstring="""
                    The end time of the interval window. Can either be defined relative to the
                    effective time or the interval start time, or as a time defined in Vault. By
                    default this will be open ended, returning unbounded results. Note:
                    care must be taken to ensure the `end` time is after the `start` time when the
                    contract code is executed; this is validated at execution time since it relies
                    on the hook `effective_time` and will result in an error during execution if
                    `start` is after `end`. The value `DefinedDateTime.INTERVAL_START` is **not**
                    allowed.
                """,
            ),
        ]


class BalancesIntervalFetcher(IntervalFetcher):
    def __init__(
        self,
        *,
        fetcher_id: str,
        start: Union[RelativeDateTime, DefinedDateTime],
        end: Optional[Union[RelativeDateTime, DefinedDateTime]] = DefinedDateTime.LIVE,
        filter: Optional[BalancesFilter] = None,
    ):
        self.class_name = self.__class__.__name__
        self.filter = filter
        super().__init__(fetcher_id=fetcher_id, start=start, end=end)

    def _validate_attributes(self):
        super()._validate_attributes()
        types_utils.validate_type(
            self.filter,
            BalancesFilter,
            is_optional=True,
            hint="BalancesFilter",
            prefix="BalancesIntervalFetcher.filter",
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        public_attributes = super()._public_attributes(language_code)
        public_attributes.append(
            types_utils.ValueSpec(
                name="filter",
                type="Optional[BalancesFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            )
        )
        return public_attributes

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="BalancesIntervalFetcher",
            docstring="""
            A fetcher for retrieving balances data within a given interval window, inclusive of
            end time.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="",
                args=cls._public_attributes(language_code),
            ),
        )



class BalancesObservationFetcher(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        fetcher_id: str,
        at: Union[DefinedDateTime, RelativeDateTime],
        filter: Optional[BalancesFilter] = None,
    ):
        self.fetcher_id = fetcher_id
        self.at = at
        self.filter = filter
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(
            self.fetcher_id,
            str,
            check_empty=True,
            hint="str",
            prefix="BalancesObservationFetcher.fetcher_id",
        )

        types_utils.validate_type(
            self.at,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[DefinedDateTime, RelativeDateTime]",
            prefix="BalancesObservationFetcher.at",
        )

        if self.at == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "BalancesObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )
        if type(self.at) is RelativeDateTime and self.at.origin == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "BalancesObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

        types_utils.validate_type(
            self.filter,
            BalancesFilter,
            hint="BalancesFilter",
            is_optional=True,
            prefix="BalancesObservationFetcher.filter",
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        public_attributes = [
            types_utils.ValueSpec(
                name="fetcher_id", type="str", docstring="The ID for this fetcher."
            ),
            types_utils.ValueSpec(
                name="at",
                type="Union[DefinedDateTime, RelativeDateTime]",
                docstring="""
                    The time at which the balances will be observed. If the value is
                    of type `DefinedDateTime`, `DefinedDateTime.INTERVAL_START`
                    is **not** allowed. If the value is of type `RelativeDateTime`,
                    `DefinedDateTime.INTERVAL_START` is **not** allowed as the `origin`.
                """,
            ),
            types_utils.ValueSpec(
                name="filter",
                type="Optional[BalancesFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            ),
        ]
        return public_attributes

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="BalancesObservationFetcher",
            docstring="A fetcher for observing balances at a given moment in time.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="",
                args=cls._public_attributes(language_code),
            ),
        )


class PostingsIntervalFetcher(IntervalFetcher):
    def __init__(
        self,
        *,
        fetcher_id: str,
        start: Union[RelativeDateTime, DefinedDateTime],
        end: Optional[Union[RelativeDateTime, DefinedDateTime]] = DefinedDateTime.LIVE,
        
    ):
        self.class_name = self.__class__.__name__
        
        super().__init__(fetcher_id=fetcher_id, start=start, end=end)

    
    

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="PostingsIntervalFetcher",
            docstring="""
                A fetcher for retrieving postings data within a given interval window, inclusive
                of end time. Note that a `PostingIntervalFetcher` does not fetch postings that
                are not committed yet.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="",
                args=cls._public_attributes(language_code),
            ),
        )


class ParametersIntervalFetcher(IntervalFetcher):
    def __init__(
        self,
        *,
        fetcher_id: str,
        start: Union[RelativeDateTime, DefinedDateTime],
        end: Optional[Union[RelativeDateTime, DefinedDateTime]] = DefinedDateTime.LIVE,
        filter: Optional[ParametersFilter] = None,
    ):
        self.class_name = self.__class__.__name__
        self.filter = filter
        super().__init__(fetcher_id=fetcher_id, start=start, end=end)

    def _validate_attributes(self):
        super()._validate_attributes()  # noqa: SLF001
        if len(self.fetcher_id) > 0 and self.fetcher_id[0] == "_":
            raise exceptions.InvalidSmartContractError(
                "ParametersIntervalFetcher 'fetcher_id' cannot start with an underscore"
            )

        if self.start == self.end:
            raise exceptions.InvalidSmartContractError(
                "ParametersIntervalFetcher 'start' cannot be equal to 'end'"
            )

        types_utils.validate_type(
            self.filter,
            ParametersFilter,
            hint="ParametersFilter",
            is_optional=True,
            prefix="ParametersIntervalFetcher.filter",
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        public_attributes = super()._public_attributes(language_code)
        # public_attributes[0] corresponds to the fetcher_id ValueSpec
        public_attributes[0].docstring += " The fetcher ID must not start with an underscore."
        public_attributes.append(
            types_utils.ValueSpec(
                name="filter",
                type="Optional[ParametersFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            ),
        )
        return public_attributes

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="ParametersIntervalFetcher",
            docstring="""
                Can only be used for `ExpectedParameters`. A fetcher for retrieving
                parameter values over an interval, inclusive of end time. In the
                `activation_hook`, if any expected parameter values are provided in the account
                creation request, these values will also be included in the parameter timeseries
                of the fetcher with `at_datetime` equal to the hook `effective_datetime`.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="",
                args=cls._public_attributes(language_code),
            ),
        )


class ParametersObservationFetcher(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        fetcher_id: str,
        at: Union[DefinedDateTime, RelativeDateTime],
        filter: Optional[ParametersFilter] = None,
    ):
        self.fetcher_id = fetcher_id
        self.at = at
        self.filter = filter
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(
            self.fetcher_id,
            str,
            check_empty=True,
            hint="str",
            prefix="ParametersObservationFetcher.fetcher_id",
        )
        if len(self.fetcher_id) > 0 and self.fetcher_id[0] == "_":
            raise exceptions.InvalidSmartContractError(
                "ParametersObservationFetcher 'fetcher_id' cannot start with an underscore"
            )

        types_utils.validate_type(
            self.at,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[DefinedDateTime, RelativeDateTime]",
            prefix="ParametersObservationFetcher.at",
        )

        if self.at == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "ParametersObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )
        if type(self.at) is RelativeDateTime and self.at.origin == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "ParametersObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

        types_utils.validate_type(
            self.filter,
            ParametersFilter,
            hint="ParametersFilter",
            is_optional=True,
            prefix="ParametersObservationFetcher.filter",
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="fetcher_id",
                type="str",
                docstring="""
                    The ID for this fetcher. The fetcher ID must not start with an underscore.
                """,
            ),
            types_utils.ValueSpec(
                name="at",
                type="Union[DefinedDateTime, RelativeDateTime]",
                docstring="""
                    The time at which the parameters will be observed. If the value is
                    of type `DefinedDateTime`, `DefinedDateTime.INTERVAL_START`
                    is **not** allowed. If the value is of type `RelativeDateTime`,
                    `DefinedDateTime.INTERVAL_START` is **not** allowed as the `origin`.
                """,
            ),
            types_utils.ValueSpec(
                name="filter",
                type="Optional[ParametersFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="ParametersObservationFetcher",
            docstring="""
                Can only be used for `ExpectedParameters`. A fetcher for observing parameter values
                at a given moment in time. In the
                `activation_hook`, if any expected parameter values are provided in the account
                creation request and if the observation time is equal to or after the hook's
                effective time, these values will override any other values in the observation.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new ParametersObservationFetcher object.",
                args=cls._public_attributes(language_code),
            ),
        )


class FlagsIntervalFetcher(IntervalFetcher):
    def __init__(
        self,
        *,
        fetcher_id: str,
        start: Union[RelativeDateTime, DefinedDateTime],
        end: Optional[Union[RelativeDateTime, DefinedDateTime]] = DefinedDateTime.LIVE,
        filter: Optional[FlagsFilter] = None,
    ):
        self.class_name = self.__class__.__name__
        self.filter = filter
        super().__init__(fetcher_id=fetcher_id, start=start, end=end)
        self._validate_attributes()

    def _validate_attributes(self):
        super()._validate_attributes()
        types_utils.validate_type(
            self.filter,
            FlagsFilter,
            is_optional=True,
            hint="FlagsFilter",
            prefix="FlagsIntervalFetcher.filter",
        )
        if self.start == self.end:
            raise exceptions.InvalidSmartContractError(
                "FlagsIntervalFetcher 'start' cannot be equal to 'end'"
            )

        # TODO(TM-91001): Remove this validation once the chronology library allows us to distinguish between
        # `LIVE` and `None` end times.
        types_utils.validate_type(
            self.end,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[RelativeDateTime, DefinedDateTime]",
            prefix="FlagsIntervalFetcher.end",
        )

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="FlagsIntervalFetcher",
            docstring="A fetcher for retrieving flags over an interval, inclusive of end time.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new FlagsIntervalFetcher object.",
                args=cls._public_attributes(language_code),
            ),
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        public_attributes = super()._public_attributes(language_code)
        public_attributes.append(
            types_utils.ValueSpec(
                name="filter",
                type="Optional[FlagsFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            ),
        )
        return public_attributes


class FlagsObservationFetcher(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        fetcher_id: str,
        at: Union[DefinedDateTime, RelativeDateTime],
        filter: Optional[FlagsFilter] = None,
    ):
        self.fetcher_id = fetcher_id
        self.at = at
        self.filter = filter
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(
            self.fetcher_id,
            str,
            check_empty=True,
            hint="str",
            prefix="FlagsObservationFetcher.fetcher_id",
        )

        types_utils.validate_type(
            self.at,
            (DefinedDateTime, RelativeDateTime),
            hint="Union[DefinedDateTime, RelativeDateTime]",
            prefix="FlagsObservationFetcher.at",
        )

        if self.at is DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "FlagsObservationFetcher 'at' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

        if type(self.at) is RelativeDateTime and self.at.origin == DefinedDateTime.INTERVAL_START:
            raise exceptions.InvalidSmartContractError(
                "FlagsObservationFetcher 'at.origin' cannot be set to 'DefinedDateTime.INTERVAL_START'"
            )

        types_utils.validate_type(
            self.filter,
            FlagsFilter,
            hint="FlagsFilter",
            is_optional=True,
            prefix="FlagsObservationFetcher.filter",
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="fetcher_id", type="str", docstring="The ID for this fetcher."
            ),
            types_utils.ValueSpec(
                name="at",
                type="Union[DefinedDateTime, RelativeDateTime]",
                docstring="""
                    The time at which the flags will be observed. If the value is
                    of type `DefinedDateTime`, `DefinedDateTime.INTERVAL_START`
                    is **not** allowed. If the value is of type `RelativeDateTime`,
                    `DefinedDateTime.INTERVAL_START` is **not** allowed as the `origin`.
                """,
            ),
            types_utils.ValueSpec(
                name="filter",
                type="Optional[FlagsFilter]",
                docstring="An optional filter to refine the results returned by the fetcher.",
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="FlagsObservationFetcher",
            docstring="A fetcher for observing flags at a given moment in time.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new FlagsObservationFetcher object.",
                args=cls._public_attributes(language_code),
            ),
        )



