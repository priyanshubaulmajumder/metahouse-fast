from decimal import Decimal

def get_decimal(value, decimal_places=4):
    if value is None:
        return None
    try:
        dp = f'.{"0"*(decimal_places-1)}1'
        return Decimal(value).quantize(Decimal(dp))
    except:
        return None

