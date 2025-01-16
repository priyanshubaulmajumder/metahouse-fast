# validator.py

from typing import Any, Dict
from app.exceptions import WealthyValidationError
from app.schemas.scheme import InvestmentTypeChoices, SchemeIdType
from app.services.service import SchemeUniqueIDsCacheService, SchemeService
from app.models.scheme import Scheme
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class RequestValidator:
    @classmethod
    async def returns_calculator(cls, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        if not (data and isinstance(data, dict)):
            raise WealthyValidationError("Invalid request: Data must be a non-empty dictionary")

        id_type = data.get('id_type')
        id_value = data.get('id_value')
        amount = data.get('amount')
        n_years = data.get('period')
        sip_day = data.get('sip_day')
        investment_type = data.get('investment_type')

        if not (id_type and id_value and amount and n_years and investment_type):
            raise WealthyValidationError("Invalid request: Missing required fields")

        investment_type = investment_type.lower() if isinstance(investment_type, str) else investment_type
        if investment_type not in InvestmentTypeChoices.values():
            raise WealthyValidationError(f"Invalid investment type: {investment_type}")

        try:
            amount = int(amount)
            n_years = int(n_years)
            if investment_type == InvestmentTypeChoices.SIP:
                sip_day = 0 if sip_day is None else min(int(str(sip_day)), 28)
        except Exception as e:
            raise WealthyValidationError(f"An error occurred during validation: {str(e)}")

        if amount < 0 or n_years < 0:
            raise WealthyValidationError("Amount and period must be positive numbers")

        wpc = await cls.validate_request_and_get_wpc(id_type=id_type, id_value=id_value, db=db)
        return {
            'wpc': wpc,
            'amount': amount,
            'n_years': n_years,
            'investment_type': investment_type,
            'sip_day': sip_day
        }

    @classmethod
    async def validate_request_and_get_wpc(cls, id_type: str, id_value: str, db: AsyncSession) -> Any:
        if not (id_type and id_value):
            raise WealthyValidationError('Invalid request')

        id_type = id_type.lower().replace('_', '-')
        if id_type not in SchemeIdType.values():
            raise WealthyValidationError('Invalid request')

        if id_type == SchemeIdType.WSchemeCode:
            resolve_result = await SchemeUniqueIDsCacheService.resolve_wpcs_from_wschemecodes(
                wschemecodes=[id_value], db=db
            )
            if resolve_result.unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolve_result.resolved[id_value]

        elif id_type == SchemeIdType.ISIN:
            resolve_result = await SchemeUniqueIDsCacheService.resolve_wpcs_from_isins(
                isins=[id_value], db=db
            )
            if resolve_result.unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolve_result.resolved[id_value]

        elif id_type == SchemeIdType.SchemeCode:
            resolve_result = await SchemeUniqueIDsCacheService.resolve_wpcs_from_scheme_codes(
                scheme_codes=[id_value], db=db
            )
            if resolve_result.unresolved:
                combinations = await SchemeUniqueIDsCacheService.get_scheme_code_combinations(scheme_code=id_value)
                for combination in combinations:
                    resolved_result = await SchemeUniqueIDsCacheService.resolve_wpcs_from_scheme_codes(
                        scheme_codes=[combination], db=db
                    )
                    if resolved_result.resolved:
                        return resolved_result.resolved[combination]
            if resolve_result.unresolved:
                raise WealthyValidationError('Scheme not found')
            return resolve_result.resolved[id_value]

        elif id_type == SchemeIdType.WPC:
            query = text(f"wpc = '{id_value}'")
        else:
            query = text(f"third_party_id = '{id_value}' and ir_scheme = False")

        schemes = await SchemeService.get_schemes_data(db=db, q=[query], allow_deprecated=True)
        scheme = next(iter(schemes), None)
        if not scheme:
            raise WealthyValidationError('Scheme not found')
        return scheme.wpc if hasattr(scheme, 'wpc') else None

