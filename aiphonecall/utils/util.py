from enum import Enum
from typing import Type



def validate_str_value(model: Type[Enum], value: Enum | str) -> Enum:
    """
    This functions validates and concert a string to an Enum.
    :param self:
    :param model:
    :param value:
    :return:
    """
    if isinstance(value, str):
        try:
            # Attempt to convert string to enum
            value = model[value.upper()]  # Convert string to enum
        except KeyError:
            # Get all valid voice names from the enum
            valid_values = ', '.join([v.name.replace("-","_") for v in model])
            raise ValueError(
                f"Invalid voice name: '{value}'.  Expected type: {model.__name__} or str with value in {valid_values}")
    elif not isinstance(value, model):
        valid_values = ', '.join([v.name.replace("-","_") for v in model])
        raise ValueError(
            f"Invalid value type: '{value}'. Expected type: {model.__name__} or str with value in {valid_values}")
    return value
