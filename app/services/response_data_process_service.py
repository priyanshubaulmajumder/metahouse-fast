from decimal import Decimal
from typing import List, Any

class ResponseDataProcessService:
    @staticmethod
    def stock_historical_prices(
        objs: List[Any], 
        fields: str = 'open,high,low,close,volume,value', 
        show_percentage_change: bool = False
    ) -> List[List[Any]]:
        if not objs:
            return []

        cols_mapping = {
            'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 
            'vol': 'volume', 'val': 'value',
            'open': 'open', 'high': 'high', 'low': 'low', 
            'close': 'close', 'volume': 'volume', 'value': 'value'
        }

        fields = [cols_mapping.get(f.strip().lower()) for f in fields.split(',')]
        fields = [f for f in fields if f is not None]

        hprices = []
        first_close_price = None

        for obj in objs:
            hprice = [str(obj.price_date)]
            hprice.extend([getattr(obj, f, None) for f in fields])

            if show_percentage_change:
                if first_close_price is None:
                    first_close_price = obj.close
                if first_close_price != 0:
                    percentage_change = ((obj.close - first_close_price) * 100) / first_close_price
                    hprice.append(round(Decimal(percentage_change), 2))
                else:
                    hprice.append(None)

            hprices.append(hprice)

        return hprices
