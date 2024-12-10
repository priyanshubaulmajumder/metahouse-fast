# validator.py

from typing import Any, Dict


from app.exceptions import WealthyValidationError
from app.schemas.scheme import InvestmentTypeChoices, SchemeIdType
from app.services.service import SchemeUniqueIDsCacheService, SchemeService

class RequestValidator:
    @classmethod
    async def returns_calculator(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if not (data and isinstance(data, dict)):
            raise WealthyValidationError("Invalid request")

        id_type = data.get('id_type')
        id_value = data.get('id_value')
        amount = data.get('amount')
        n_years = data.get('period')
        sip_day = data.get('sip_day')
        investment_type = data.get('investment_type')

        if not (id_type and id_value and amount and n_years and investment_type):
            raise WealthyValidationError("Invalid request")

        investment_type = investment_type.lower()
        if investment_type not in InvestmentTypeChoices.values.keys():
            raise WealthyValidationError("Invalid request")

        try:
            amount = int(amount)
            n_years = int(n_years)
            if investment_type == InvestmentTypeChoices.Sip:
                sip_day = min(int(sip_day), 28)
        except Exception:
            raise WealthyValidationError("Invalid request")

        if amount < 0 or n_years < 0:
            raise WealthyValidationError("Invalid request")

        wpc = await cls.validate_request_and_get_wpc(id_type=id_type, id_value=id_value)
        return {
            'wpc': wpc,
            'amount': amount,
            'n_years': n_years,
            'investment_type': investment_type,
            'sip_day': sip_day
        }

    @staticmethod
    async def validate_request_and_get_wpc(id_type: str, id_value: str) -> Any:
        if not (id_type and id_value):
            raise WealthyValidationError('Invalid request')

        id_type = id_type.lower().replace('_', '-')
        if id_type not in SchemeIdType.values.keys():
            raise WealthyValidationError('Invalid request')

        if id_type == SchemeIdType.WSchemeCode:
            resolved, resolved_new_wpcs, unresolved = await SchemeUniqueIDsCacheService.resolve_wpcs_from_wschemecodes(
                wschemecodes=[id_value]
            )
            if unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolved[id_value]

        elif id_type == SchemeIdType.ISIN:
            resolved, resolved_new_wpcs, unresolved = await SchemeUniqueIDsCacheService.resolve_wpcs_from_isins(
                isins=[id_value]
            )
            if unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolved[id_value]

        elif id_type == SchemeIdType.SchemeCode:
            resolved, resolved_new_wpcs, unresolved = await SchemeUniqueIDsCacheService.resolve_wpcs_from_scheme_codes(
                scheme_codes=[id_value]
            )
            if unresolved:
                combinations = await SchemeUniqueIDsCacheService.get_scheme_code_combinations(scheme_code=id_value)
                for combination in combinations:
                    resolved, resolved_new_wpcs, unresolved = await SchemeUniqueIDsCacheService.resolve_wpcs_from_scheme_codes(
                        scheme_codes=[combination]
                    )
                    if resolved:
                        return resolved[combination]
            if unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolved[id_value]

        elif id_type == SchemeIdType.WPC:
            q = {'wpc__iexact': id_value}
        else:
            q = {'third_party_id__iexact': id_value, 'ir_scheme': False}

        # Assuming 'get_schemes_data' is an async method returning an iterable
        schemes = await SchemeService.get_schemes_data(q=q, allow_deprecated=True)
        scheme = next(iter(schemes), None)
        if not scheme:
            raise WealthyValidationError('Scheme not found')
        return scheme.wpc