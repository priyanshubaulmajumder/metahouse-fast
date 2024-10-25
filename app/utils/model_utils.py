import shortuuid
from sqlalchemy import String, TypeDecorator
from sqlalchemy.orm import declared_attr

class WealthyExternalIdField(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, prefix='', auto=True, *args, **kwargs):
        self.auto = auto
        self.prefix = prefix
        kwargs['length'] = 50
        super(WealthyExternalIdField, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if self.auto and not value:
            return self.prefix + shortuuid.uuid()
        return value

class WealthyProductCodeField(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, prefix, Modal, max_length=12, *args, **kwargs):
        self.prefix = prefix
        self.Modal = Modal
        self.max_length = max_length
        kwargs['length'] = max_length
        super(WealthyProductCodeField, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if not value:
            # This part needs to be handled in the model's __init__ or before_insert event
            return None
        return value

    @classmethod
    def generate_code(cls, session, prefix, Modal, max_length):
        modal_instance = Modal()
        session.add(modal_instance)
        session.flush()
        generated_id = modal_instance.generated_id
        return f"{prefix}{generated_id:0{max_length-len(prefix)}d}"

def generate_wealthy_stock_code(stock):
    if stock.isin:
        return stock.isin
    return "wstc_" + shortuuid.uuid()
