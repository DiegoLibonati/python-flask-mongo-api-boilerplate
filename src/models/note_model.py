from typing import Annotated

from pydantic import BaseModel, StringConstraints


class NoteModel(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
