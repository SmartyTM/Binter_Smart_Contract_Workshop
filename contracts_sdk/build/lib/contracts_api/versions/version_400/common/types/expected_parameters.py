from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from typing import List, Optional, Union

from .enums import DateTimePrecision

from ...common.docs import _common_docs_path
from .....utils import exceptions, symbols, types_utils
from .....utils.timezone_utils import validate_timezone_is_utc

# <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
from .....utils.feature_flags import (
    POST_PARAMETER_IMPROVEMENTS,
    is_fflag_enabled,
)

# <NOT RELEASE END>


class Constraint(types_utils.ContractsLanguageDunderMixin):
    pass


class StringConstraint(Constraint):
    def __init__(
        self,
        *,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        super().__init__()
        self.min_length = min_length
        self.max_length = max_length
        self._validate_attributes()

    def _validate_attributes(self):
        if self.min_length is None:
            self.min_length = 0

        # self.max_length = 0 means no maximum length
        if self.max_length is None:
            self.max_length = 0

        types_utils.validate_type(self.min_length, int)
        types_utils.validate_type(self.max_length, int)
        if self.min_length < 0:
            raise exceptions.InvalidSmartContractError(
                f"StringConstraint min_length must be non-negative (received {self.min_length})",
            )
        if self.max_length < 0:
            raise exceptions.InvalidSmartContractError(
                f"StringConstraint max_length must be non-negative (received {self.max_length})",
            )
        if self.max_length != 0 and self.min_length > self.max_length:
            raise exceptions.InvalidSmartContractError(
                "StringConstraint min_length must be less than or equal to max_length "
                f"(received {self.min_length} > {self.max_length})",
            )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="min_length",
                type="Optional[int]",
                docstring="The minimum length (inclusive) of the string value.",
            ),
            types_utils.ValueSpec(
                name="max_length",
                type="Optional[int]",
                docstring="The maximum length (inclusive) of the string value. "
                "A value of 0 is interpreted as no maximum length.",
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="StringConstraint",
            docstring="""
            A Constraint indicating that an expected parameter must be a string.

            Note: This only applies to Core API Parameters. For the Smart Contract Parameters shape
            equivalent, see _Parameter shape to constraint mapping_ in the 
            [Data changes when using the Parameters resource](/vault_v5/parameters/#parameter_changes_in_vault_5-data_changes_when_using_the_parameters_resource) section.

            The return value of a parameter with this constraint in the Smart Contract
            ParameterValueTimeseries is of the type str or None.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new StringConstraint object.",
                args=cls._public_attributes(language_code),
            ),
        )


class DateTimeConstraint(Constraint):
    def __init__(
        self,
        *,
        precision: Optional[DateTimePrecision] = None,
        earliest: Optional[datetime] = None,
        latest: Optional[datetime] = None,
    ):
        super().__init__()
        self.precision = precision
        self.earliest = earliest
        self.latest = latest
        self._validate_attributes()

    def _validate_attributes(self):
        if self.precision is not None:
            types_utils.validate_type(
                self.precision,
                DateTimePrecision,
                hint="DateTimePrecision value",
                prefix="precision",
            )
        if self.latest is not None:
            types_utils.validate_type(self.latest, datetime, prefix="latest")
            validate_timezone_is_utc(
                self.latest,
                "latest",
                "DateTimeConstraint",
            )
        if self.earliest is not None:
            types_utils.validate_type(self.earliest, datetime, prefix="earliest")
            validate_timezone_is_utc(
                self.earliest,
                "earliest",
                "DateTimeConstraint",
            )
            if self.latest is not None and self.earliest > self.latest:
                raise exceptions.InvalidSmartContractError(
                    "DateTimeConstraint earliest must be no later than latest "
                    f"(received {self.earliest} > {self.latest})",
                )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="precision",
                type="Optional[DateTimePrecision]",
                docstring="Shortest time denomination that can be set.",
            ),
            types_utils.ValueSpec(
                name="earliest",
                type="Optional[datetime]",
                docstring="""
                    The earliest permitted datetime. Must be a timezone-aware UTC datetime
                    using the ZoneInfo class.
                """,
            ),
            types_utils.ValueSpec(
                name="latest",
                type="Optional[datetime]",
                docstring="""
                    The latest permitted datetime. Must be a timezone-aware UTC datetime
                    using the ZoneInfo class.
                """,
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="DateTimeConstraint",
            docstring="""
            A Constraint indicating that an expected parameter must be
            in date-time format.

            Note: This only applies to Core API Parameters. For the Smart Contract Parameters shape
            equivalent, see _Parameter shape to constraint mapping_ in the 
            [Data changes when using the Parameters resource](/vault_v5/parameters/#parameter_changes_in_vault_5-data_changes_when_using_the_parameters_resource) section.

            The return value of a parameter with this constraint in the Smart Contract
            ParameterValueTimeseries is of the type datetime or None.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new DateTimeConstraint object.",
                args=cls._public_attributes(language_code),
            ),
        )


class DecimalConstraint(Constraint):
    def __init__(
        self,
        *,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
    ):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self._validate_attributes()

    def _validate_attributes(self):
        if self.min_value is not None:
            types_utils.validate_type(self.min_value, Decimal, prefix="min_value")
        if self.max_value is not None:
            types_utils.validate_type(self.max_value, Decimal, prefix="max_value")
        if (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value > self.max_value
        ):
            raise exceptions.InvalidSmartContractError(
                "DecimalConstraint 'min_value' must be less than or equal to 'max_value' "
                f"(received {self.min_value} > {self.max_value})",
            )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="min_value",
                type="Optional[Decimal]",
                docstring="The minimum value (inclusive) that the number can be.",
            ),
            types_utils.ValueSpec(
                name="max_value",
                type="Optional[Decimal]",
                docstring="The maximum value (inclusive) that the number can be.",
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="DecimalConstraint",
            docstring="""
            A Constraint indicating that an expected parameter must be a Decimal.

            Note: This only applies to Core API Parameters. For the Smart Contract Parameters shape
            equivalent, see _Parameter shape to constraint mapping_ in the 
            [Data changes when using the Parameters resource](/vault_v5/parameters/#parameter_changes_in_vault_5-data_changes_when_using_the_parameters_resource) section.

            The return value of a parameter with this constraint in the Smart Contract
            ParameterValueTimeseries is of the type Decimal or None.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new DecimalConstraint object.",
                args=cls._public_attributes(language_code),
            ),
        )


class EnumerationConstraint(Constraint):
    def __init__(
        self,
        *,
        permitted_values: List[str],
    ):
        super().__init__()
        self.permitted_values = permitted_values
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(self.permitted_values, list, prefix="permitted_values")

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="permitted_values",
                type="List[str]",
                docstring="The list of permitted values for the parameter.",
            ),
        ]

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="EnumerationConstraint",
            docstring="""
            A Constraint indicating that an expected parameter must be one of a set of values.

            Note: This only applies to Core API Parameters. For the Smart Contract Parameters shape
            equivalent, see _Parameter shape to constraint mapping_ in the 
            [Data changes when using the Parameters resource](/vault_v5/parameters/#parameter_changes_in_vault_5-data_changes_when_using_the_parameters_resource) section.

            The return value of a parameter with this constraint in the Smart Contract
            ParameterValueTimeseries is of the type str or None.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new EnumerationConstraint object.",
                args=cls._public_attributes(language_code),
            ),
        )


class AccountConstraint(Constraint):
    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")
        return []

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="AccountConstraint",
            docstring="""
            A Constraint indicating that an expected parameter must be the ID of an
            existing Account.

            Note: This only applies to Core API Parameters. For the Smart Contract Parameters shape
            equivalent, see _Parameter shape to constraint mapping_ in the 
            [Data changes when using the Parameters resource](/vault_v5/parameters/#parameter_changes_in_vault_5-data_changes_when_using_the_parameters_resource) section.

            The return value of a parameter with this constraint in the Smart Contract
            ParameterValueTimeseries is of the type str or None.
            """,
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new AccountConstraint object.",
                args=cls._public_attributes(language_code),
            ),
        )


class ExpectedParameter(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        id: str,
        constraint: Optional[
            Union[
                AccountConstraint,
                DateTimeConstraint,
                DecimalConstraint,
                EnumerationConstraint,
                StringConstraint,
            ]
        ] = None,  # noqa: E501
        triggers_pre_parameter_change_hook: Optional[bool] = None,
        optional: Optional[bool] = False,
        # <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
        *,
        triggers_post_parameter_change_hook: Optional[bool] = None,
        # <NOT RELEASE END>
    ):
        self.id = id
        self.constraint = constraint
        self.optional = optional
        self.triggers_pre_parameter_change_hook = triggers_pre_parameter_change_hook
        # <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
        if is_fflag_enabled(POST_PARAMETER_IMPROVEMENTS):
            self.triggers_post_parameter_change_hook = triggers_post_parameter_change_hook
        # <NOT RELEASE END>
        self._validate_attributes()

    def _validate_attributes(self):
        if not self.id:
            raise exceptions.InvalidSmartContractError("ExpectedParameter 'id' must be populated")
        if self.constraint is not None:
            hint = (
                "Optional[Union[AccountConstraint, DateTimeConstraint, DecimalConstraint, "
                "EnumerationConstraint, StringConstraint]]"
            )
            types_utils.validate_type(self.constraint, Constraint, hint=hint)
        types_utils.validate_type(self.optional, bool, is_optional=True, hint="Optional[bool]")
        types_utils.validate_type(
            self.triggers_pre_parameter_change_hook, bool, is_optional=True, hint="Optional[bool]"
        )
        # <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
        if is_fflag_enabled(POST_PARAMETER_IMPROVEMENTS):
            types_utils.validate_type(
                self.triggers_post_parameter_change_hook,
                bool,
                is_optional=True,
                hint="Optional[bool]",
            )
            self._validate_hook_execution_args(
                self.triggers_pre_parameter_change_hook, self.triggers_post_parameter_change_hook
            )
        # <NOT RELEASE END>

    # <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
    def _validate_hook_execution_args(
        self, pre_posting: Optional[bool], post_posting: Optional[bool]
    ) -> None:
        if post_posting is not None and pre_posting is None:
            raise ValueError(
                f"Parameter with id={self.id}: triggers_pre_parameter_change_hook must be explicitly "
                "defined if triggers_post_parameter_change_hook is explicitly defined."
            )

    # <NOT RELEASE END>

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="ExpectedParameter",
            docstring="Defines a Parameter which is expected to have been created "
            "using the Parameters API.",
            public_attributes=cls._public_attributes(language_code),  # noqa SLF001
            constructor=types_utils.ConstructorSpec(
                docstring="Constructs a new ExpectedParameter.",
                args=cls._public_attributes(language_code),  # noqa SLF001
            ),
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        public_attributes = [
            types_utils.ValueSpec(
                name="id",
                type="str",
                docstring="The ID of the Parameter.",
            ),
            types_utils.ValueSpec(
                name="constraint",
                type="Optional[Union[AccountConstraint, DateTimeConstraint, DecimalConstraint, "
                "EnumerationConstraint, StringConstraint]]",
                docstring="The type and any extra validation that applies to this parameter. "
                "If provided, must exactly match the constraint provided when creating "
                "this parameter.",
            ),
            types_utils.ValueSpec(
                name="triggers_pre_parameter_change_hook",
                type="Optional[bool]",
                docstring="Determines whether changes to account-owned parameter values for this "
                "parameter will trigger the `pre_parameter_change_hook`. Defaults to True.",
            ),
            types_utils.ValueSpec(
                name="optional",
                type="Optional[bool]",
                docstring="Whether this Parameter should always have a value. If set to True, then "
                "the timeseries returned from get_parameter_timeseries for this parameter may have "
                "entries set to None, and entries in the result of get_parameters_observation for "
                "this parameter may be None. If set to False, then REST API requests that would "
                "leave this parameter without a value will result in an HTTP 400 status response "
                "(exceptions apply, see "
                f"[ParameterValueTimeseries]({_common_docs_path}classes/#ParameterValueTimeseries) "
                "for details). Defaults to False.",
            ),
        ]
        # <NOT RELEASE START: IMP_2_POST_PARAMETER_IMPROVEMENTS>
        if is_fflag_enabled(POST_PARAMETER_IMPROVEMENTS):
            public_attributes.append(
                types_utils.ValueSpec(
                    name="triggers_post_parameter_change_hook",
                    type="Optional[bool]",
                    docstring="Determines whether changes to this parameter trigger the "
                    "`post_parameter_change_hook`. "
                    "If explicitly defined, then `triggers_pre_parameter_change_hook` must also be "
                    "explicitly defined, and both arguments must be defined for every ExpectedParameter "
                    "defined in the Smart Contract. Defaults to True.",
                )
            )
        # <NOT RELEASE END>
        return public_attributes
