import shortuuid
from sqlalchemy import String, TypeDecorator
from sqlalchemy.orm import declared_attr,Session

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

    def __init__(self, prefix='', Modal=None, auto=True, max_length=12, *args, **kwargs):
        self.auto = auto
        self.prefix = prefix
        self.Modal = Modal
        self.max_length = max_length
        kwargs['length'] = max_length
        super(WealthyProductCodeField, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if self.auto and not value:
            return None  # Value will be generated in the model's __init__ or before_insert event
        return value

    def id_generator(self, session: Session):
        if not self.Modal:
            return None
        modal_instance = self.Modal()
        session.add(modal_instance)
        session.flush()
        generated_id = modal_instance.generated_id
        return f"{self.prefix}{'0'*(self.max_length-len(self.prefix)-len(str(generated_id)))}{generated_id}"

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        """
        value = getattr(model_instance, self.key)
        if self.auto and not value:
            session = Session.object_session(model_instance)
            value = str(self.id_generator(session))
            setattr(model_instance, self.key, value)
        return value

    def formfield(self, **kwargs):
        if self.auto:
            return None
        return super(WealthyProductCodeField, self).formfield(**kwargs)
    
def generate_wealthy_stock_code(stock):
    if stock.isin:
        return stock.isin
    return "wstc_" + shortuuid.uuid()

def generate_wealthy_mf_code(fund):
    if fund.isin:
        return fund.isin
    amc_code = getattr(fund, 'amc', None)
    plan_type = getattr(fund, 'plan_type', None)
    return_type = getattr(fund, 'return_type', None)
    scheme_code = getattr(fund, 'scheme_code', None)
    if amc_code and return_type and plan_type and scheme_code:
        wealthy_code = "M" + amc_code + scheme_code + return_type + plan_type
    else:
        wealthy_code = "wsc_" + shortuuid.uuid()
    return wealthy_code
