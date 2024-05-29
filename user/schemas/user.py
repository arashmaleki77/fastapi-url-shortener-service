from pydantic import BaseModel, constr, ConfigDict
from datetime import datetime
from typing import Optional


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: constr(min_length=5, max_length=25)
    sub_directory: constr(min_length=5, max_length=150)
    first_name: Optional[constr(max_length=25)]
    last_name: Optional[constr(max_length=25)]
    created_at: datetime
    updated_at: datetime
