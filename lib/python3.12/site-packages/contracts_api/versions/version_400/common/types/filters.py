from functools import lru_cache


from .....utils import exceptions, symbols, types_utils
from typing import List


class BalancesFilter(types_utils.ContractsLanguageDunderMixin):
    def __init__(self, *, addresses: List[str]):
        self.addresses = addresses
        self._validate_attributes()

    def _validate_attributes(self):
        type_hint = "str"
        iterator = types_utils.get_iterator(
            self.addresses, type_hint, "addresses", check_empty=True
        )
        for address in iterator:
            types_utils.validate_type(address, str, hint=f"List[{type_hint}]")
        if len(self.addresses) < 1:
            raise exceptions.InvalidSmartContractError(
                "BalancesFilter addresses must contain at least one address."
            )
        if len(set(self.addresses)) != len(self.addresses):
            raise exceptions.InvalidSmartContractError(
                "BalancesFilter addresses must not contain any duplicate addresses."
            )

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return types_utils.ClassSpec(
            name="BalancesFilter",
            docstring="A filter for refining the balances data retrieved by a fetcher.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="", args=cls._public_attributes(language_code)
            ),
        )

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="addresses", type="List[str]", docstring="A list of balance addresses."
            ),
        ]


class ParametersFilter(types_utils.ContractsLanguageDunderMixin):
    def __init__(self, *, parameter_ids: List[str]):
        self.parameter_ids = parameter_ids
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(
            self.parameter_ids, list, hint="List[str]", prefix="ParametersFilter.parameter_ids"
        )
        for item in types_utils.get_iterator(
            self.parameter_ids, hint="str", name="ParametersFilter.parameter_ids", check_empty=True
        ):
            types_utils.validate_type(
                item, str, hint="str", prefix="ParametersFilter.parameter_ids"
            )

        if len(self.parameter_ids) < 1:
            raise exceptions.InvalidSmartContractError(
                "ParametersFilter parameter_ids must contain at least one parameter id."
            )

        if len(set(self.parameter_ids)) != len(self.parameter_ids):
            raise exceptions.InvalidSmartContractError(
                "ParametersFilter parameter_ids must not contain any duplicate parameter ids."
            )

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        spec = types_utils.ClassSpec(
            name="ParametersFilter",
            docstring="A filter for refining the parameters retrieved by a fetcher. Each ID here "
            "must correspond to the ID of an ExpectedParameter defined in the contract metadata.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="", args=cls._public_attributes(language_code)
            ),
        )
        return spec

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="parameter_ids",
                type="List[str]",
                docstring="A list of parameter IDs to fetch",
            ),
        ]


class FlagsFilter(types_utils.ContractsLanguageDunderMixin):
    def __init__(self, *, flag_definition_ids: List[str]):
        self.flag_definition_ids = flag_definition_ids
        self._validate_attributes()

    def _validate_attributes(self):
        types_utils.validate_type(
            self.flag_definition_ids,
            list,
            hint="List[str]",
            prefix="FlagsFilter.flag_definition_ids",
        )
        iterator = types_utils.get_iterator(
            self.flag_definition_ids,
            hint="str",
            name="FlagsFilter.flag_definition_ids",
            check_empty=True,
        )
        for item in iterator:
            types_utils.validate_type(
                item, str, hint="str", prefix="FlagsFilter.flag_definition_ids"
            )

        if len(set(self.flag_definition_ids)) != len(self.flag_definition_ids):
            raise exceptions.InvalidSmartContractError(
                "FlagsFilter flag_definition_ids must not contain any duplicate flag definition"
                " ids."
            )

    @classmethod
    @lru_cache()
    def _spec(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        spec = types_utils.ClassSpec(
            name="FlagsFilter",
            docstring="A filter for refining the flags retrieved by a fetcher.",
            public_attributes=cls._public_attributes(language_code),
            constructor=types_utils.ConstructorSpec(
                docstring="", args=cls._public_attributes(language_code)
            ),
        )
        return spec

    @classmethod
    @lru_cache()
    def _public_attributes(cls, language_code=symbols.Languages.ENGLISH):
        if language_code != symbols.Languages.ENGLISH:
            raise ValueError("Language not supported")

        return [
            types_utils.ValueSpec(
                name="flag_definition_ids",
                type="List[str]",
                docstring="A list of flag definition ids to get flags for.",
            ),
        ]



