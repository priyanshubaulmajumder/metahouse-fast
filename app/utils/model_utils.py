import shortuuid
from sqlalchemy import String, TypeDecorator, Column, event
from sqlalchemy.orm import declared_attr,Session
from typing import Any

import shortuuid
from sqlalchemy import Column, String, event
from typing import Any

class WealthyExternalIdField:
    def __init__(self, prefix: str = '', auto: bool = True, *args: Any, **kwargs: Any):
        self.auto = auto
        self.prefix = prefix
        max_length = kwargs.pop('max_length', 50)
        self._name = None  # Will be set in __set_name__
        self.column = Column(String(max_length), *args, **kwargs)
        if self.auto:
            self.column.default = self.shortuuid_generator
            self.column.unique = True
            self.column.nullable = False
            self.column.primary_key = kwargs.get('primary_key', False)

    def __set_name__(self, owner, name):
        """
        Called when the descriptor is assigned to an owner class.
        """
        self._name = name
        self.column.name = name  # Assign the column name
        if self.auto:
            # Attach the event listener to the owner class (mapper)
            event.listen(
                owner,
                'before_insert',
                self.generate_uuid_before_insert
            )

    def shortuuid_generator(self) -> str:
        return self.prefix + shortuuid.uuid()

    def generate_uuid_before_insert(self, mapper, connection, target):
        """
        Event listener to generate the UUID before insert.
        """
        value = getattr(target, self._name)
        if not value:
            value = self.shortuuid_generator()
            setattr(target, self._name, value)

    def __get__(self, instance, owner):
        """
        Descriptor protocol to access the column attribute.
        """
        return self.column

    def __set__(self, instance, value):
        """
        Descriptor protocol to set the value of the column.
        """
        setattr(instance, self._name, value)

    def __getattr__(self, item):
        # Delegate attribute access to the underlying Column
        return getattr(self.column, item)

    def __repr__(self):
        return f"WealthyExternalIdField(prefix='{self.prefix}', auto={self.auto})"

    def __str__(self):
        return self.__repr__()


from sqlalchemy import Column, String, event
from sqlalchemy.orm import Session, attributes
from typing import Any

class WealthyProductCodeField:
    def __init__(
        self,
        prefix: str = '',
        Modal=None,
        auto: bool = True,
        max_length: int = 50,
        *args: Any,
        **kwargs: Any
    ):
        self.auto = auto
        self.prefix = prefix
        self.Modal = Modal
        self._name = None  # Will be set in __set_name__
        self.column = Column(String(max_length), *args, **kwargs)
        if self.auto:
            self.column.nullable = False
            self.column.unique = True
            self.column.primary_key = kwargs.get('primary_key', False)

    def __set_name__(self, owner, name):
        # Called when the descriptor is assigned to an owner class.
        self._name = name
        self.column.name = name
        if self.auto:
            # Attach the event listener to the owner class
            event.listen(
                owner,
                'before_insert',
                self.generate_code_before_insert
            )
        # Add the column to the class mapper
        if hasattr(owner, '__mapper__'):
            owner.__mapper__.add_property(name, self.column)
        else:
            setattr(owner, name, self.column)

    def id_generator(self, session: Session):
        if not self.Modal:
            return None
        modal_instance = self.Modal()
        session.add(modal_instance)
        session.flush()
        generated_id = modal_instance.generated_id
        zero_padding = '0' * (8 - len(str(generated_id)))
        return f"{self.prefix}{zero_padding}{generated_id}"

    def generate_code_before_insert(self, mapper, connection, target):
        # Event listener to generate the code before insert.
        value = getattr(target, self._name)
        if self.auto and not value:
            session = Session.object_session(target)
            if session is None:
                raise Exception("Session not found. Cannot generate code.")
            value = str(self.id_generator(session))
            setattr(target, self._name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self.column
        # Access the value directly from the instance state
        return attributes.instance_state(instance).dict.get(self._name)

    def __set__(self, instance, value):
        # Set the value directly in the instance state
        attributes.instance_state(instance).dict[self._name] = value

    def __getattr__(self, item):
        # Delegate attribute access to the underlying Column.
        return getattr(self.column, item)
    
    
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

