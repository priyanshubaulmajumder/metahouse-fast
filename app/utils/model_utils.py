import shortuuid
from sqlalchemy import String, TypeDecorator, Column, event
from sqlalchemy.orm import declared_attr,Session

# class WealthyExternalIdField(TypeDecorator):
#     impl = String
#     cache_ok = True

#     def __init__(self, prefix='', auto=True, *args, **kwargs):
#         self.auto = auto
#         self.prefix = prefix
#         kwargs['length'] = 50
#         super(WealthyExternalIdField, self).__init__(*args, **kwargs)

#     def process_bind_param(self, value, dialect):
#         if self.auto and not value:
#             return self.prefix + shortuuid.uuid()
#         return value
    

# class WealthyExternalIdField(models.CharField):
#     """
#     A field which stores a Short UUID value in base57 format. This may also have
#     the Boolean attribute 'auto' which will set the value on initial save to a
#     new UUID value (calculated using shortuuid's default (uuid4)). Note that while all
#     UUIDs are expected to be unique we enforce this with a DB constraint.
#     """

#     def shortuuid_generator(self):
#         return self.prefix + shortuuid.uuid()

#     def __init__(self, prefix='', auto=True, *args, **kwargs):
#         self.auto = auto
#         self.prefix = prefix
#         # We store UUIDs in base57 format, which is fixed at 22 characters. Also added some extra characters for storing prefix.
#         kwargs['max_length'] = 50
#         if auto:
#             # Do not let the user edit UUIDs if they are auto-assigned.
#             kwargs['editable'] = False
#             kwargs['unique'] = True

#         super(WealthyExternalIdField, self).__init__(*args, **kwargs)

#     def pre_save(self, model_instance, add):
#         """
#         This is used to ensure that we auto-set values if required.
#         See CharField.pre_save
#         """
#         value = super(WealthyExternalIdField, self).pre_save(model_instance, add)
#         if self.auto and not value:
#             # Assign a new value for this attribute if required.
#             value = str(self.shortuuid_generator())
#             setattr(model_instance, self.attname, value)
#         return value

#     def formfield(self, **kwargs):
#         if self.auto:
#             return None
#         return super(WealthyExternalIdField, self).formfield(**kwargs)



#hehehehehehehehhhhhhhhhhhhhhhhhhhhhhehehehehehehehehehehehehehe


class WealthyExternalIdField:
    def __init__(self, prefix: str = '', auto: bool = True, *args: Any, **kwargs: Any):
        """
        A field which stores a Short UUID value in base57 format. This may also have
        the Boolean attribute 'auto' which will set the value on initial save to a
        new UUID value (calculated using shortuuid's default (uuid4)).
        Note that while all UUIDs are expected to be unique; we enforce this with a DB constraint.
        """
        self.auto = auto
        self.prefix = prefix
        # We store UUIDs in base57 format, which is fixed at 22 characters.
        # Also added extra characters for storing prefix.
        max_length = kwargs.pop('max_length', 50)
        self.column = Column(String(max_length), *args, **kwargs)
        if self.auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            self.column.unique = True
            self.column.nullable = False
            self.column.default = self.shortuuid_generator
            self.column.primary_key = kwargs.get('primary_key', False)
            event.listen(
                self.column,                                                
                'before_insert',
                self.generate_uuid_before_insert,
                retval=True
            )

    def shortuuid_generator(self) -> str:
        return self.prefix + shortuuid.uuid()

    def generate_uuid_before_insert(self, mapper, connection, target):
        """
        This is used to ensure that we auto-set values if required.
        """
        value = getattr(target, self.column.name)
        if self.auto and not value:
            # Assign a new value for this attribute if required.
            value = str(self.shortuuid_generator())
            setattr(target, self.column.name, value)
        return value

    def __getattr__(self, item):
        # Delegate attribute access to the underlying Column
        return getattr(self.column, item)

    def __repr__(self):
        return f"WealthyExternalIdField(prefix='{self.prefix}', auto={self.auto})"

    def __str__(self):
        return self.__repr__()
    
        
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
