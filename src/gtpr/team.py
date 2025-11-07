import pydantic


class Team(pydantic.BaseModel):
    name: str
    skill: str
