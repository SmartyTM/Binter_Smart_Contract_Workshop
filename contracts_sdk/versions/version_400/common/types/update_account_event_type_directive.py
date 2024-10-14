from functools import lru_cache

from ...common.docs import _common_docs_path
from .....utils import symbols
from .....utils import types_utils
from .....utils.exceptions import InvalidSmartContractError, StrongTypingError
from .....utils.timezone_utils import validate_datetime_is_timezone_aware

from .event_types import ScheduleExpression, ScheduleSkip
from .schedules import EndOfMonthSchedule

from datetime import datetime
from typing import Union, Optional


class UpdateAccountEventTypeDirective(types_utils.ContractsLanguageDunderMixin):
    def __init__(
        self,
        *,
        event_type: str,
        expression: Optional[ScheduleExpression] = None,
        schedule_method: Optional[EndOfMonthSchedule] = None,
        end_datetime: Optional[datetime] = None,
        skip: Optional[Union[bool, ScheduleSkip]] = None,
        _from_proto: bool = False,
    ):
        self.event_type = event_type
        self.expression = expression
        self.end_datetime = end_datetime
        self.skip = skip
        self.schedule_method = schedule_method
        if not _from_proto:
            self._validate_attributes()

    def _validate_attributes(self):
        if self.expression is not None:
            types_utils.validate_type(self.expression, ScheduleExpression)
        if self.schedule_method is not None:
            types_utils.validate_type(self.schedule_method, EndOfMonthSchedule)
        if self.end_datetime is not None:
            types_utils.validate_type(self.end_datetime, datetime)
            validate_datetime_is_timezone_aware(
                self.end_datetime,
                "end_datetime",
                "UpdateAccountEventTypeDirective",
            )
        if self.skip is None:
            if not self.end_datetime and not self.expression and not self.schedule_method:
                raise InvalidSmartContractError(
                    "UpdateAccountEventTypeDirective object must have either an "
                    "end_datetime, an expression, schedule_method, or skip defined"
                )
        else:
            try:
                types_utils.validate_type(self.skip, bool)
            except StrongTypingError:
                types_utils.validate_type(
                    self.skip,
                    ScheduleSkip,
                    prefix="skip",
                    hint="Optional[Union[bool, ScheduleSkip]]",
                )
        if self.expression is not None and self.schedule_method is not None:
            raise InvalidSmartContractError(
                "UpdateAccountEventTypeDirective cannot contain both"
                " expression and schedule_method fields"
            )

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")
        return types_utils.ClassSpec(
            name="UpdateAccountEventTypeDirective",
            docstring="",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="A Hook Directive that instructs updating an Account Event Type.",
                args=cls._public_attributes(language_code),
            ),
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")
        return [
            types_utils.ValueSpec(
                name="event_type", type="str", docstring="The `event_type` that is to be modified."
            ),
            types_utils.ValueSpec(
                name="expression",
                type="Optional[ScheduleExpression]",
                docstring=f"""
                    Optional [ScheduleExpression]({_common_docs_path}classes/#ScheduleExpression).
                    Either `expression` or `schedule_method` must be populated.
                """,
            ),
            types_utils.ValueSpec(
                name="schedule_method",
                type="Optional[EndOfMonthSchedule]",
                docstring=f"""
                    Optional [EndOfMonthSchedule]({_common_docs_path}classes/#EndOfMonthSchedule).
                    Either `expression` or `schedule_method` must be populated.
                """,
            ),
            types_utils.ValueSpec(
                name="end_datetime",
                type="Optional[datetime]",
                docstring="""
                    Optional datetime that indicates when the schedule should stop executing.
                    Must be timezone aware using the `ZoneInfo` class and be based
                    on the Account's operating timezone. The
                    [events_timezone](/reference/contracts/contracts_api_4xx/smart_contracts_api_reference4xx/vault/#attributes-events_timezone)
                    is inherited from the
                    [Processing Group](/vault_v5/processing_groups/#what_is_a_processing_group),
                    if set. Otherwise it can be set as a field defined in the
                    [Smart Contract metadata](../../smart_contracts_api_reference4xx/metadata/#events_timezone).
                    If neither of these is set,
                    [vault.events_timezone](/reference/contracts/contracts_api_4xx/smart_contracts_api_reference4xx/vault/#attributes-events_timezone)
                    defaults to UTC. When reinstructing from a supervisor contract, the plan's
                    [vault.events_timezone](/reference/contracts/contracts_api_4xx/supervisor_contracts_api_reference4xx/vault/#attributes-events_timezone)
                    must match the account's
                    [vault.events_timezone](/reference/contracts/contracts_api_4xx/smart_contracts_api_reference4xx/vault/#attributes-events_timezone).
                    Note that once the `end_datetime` has been reached, the schedule can
                    **no longer** be updated or re-enabled
                """,  # noqa: E501
            ),
            types_utils.ValueSpec(
                name="skip",
                type="Optional[Union[bool, ScheduleSkip]]",
                docstring="""
                    An optional flag to skip a schedule indefinitely (True), unskip a
                    Schedule (False), or to skip until a specified time (ScheduleSkip).
                """,
            ),
        ]
