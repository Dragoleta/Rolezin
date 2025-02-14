import random
import string

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


def generateCode(length: int = 6) -> str:
    assert length is not None, "Lenght does not exist"
    assert isinstance(length, int), f"Length should be a integer got {length.__class__}"
    assert length > 0, f"Length should be higher than 0 got { length } instead"

    random_string = "".join(random.choices(string.ascii_lowercase, k=length))
    return random_string
