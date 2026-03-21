from collections import UserList

from pydantic import BaseModel, field_validator


class SkillsList(UserList):
    @property
    def names(self):
        return [skill.name for skill in self if skill.name.lower() != 'overall']

    @property
    def xp(self):
        return [skill.xp for skill in self if skill.name.lower() != 'overall']

    @property
    def levels(self):
        return [skill.level for skill in self if skill.name.lower() != 'overall']


class Skill(BaseModel):
    id: int
    name: str
    rank: int
    level: int
    xp: int


class Player(BaseModel):
    name: str
    skills: list[Skill]

    @field_validator('skills', mode='after')
    def build_skills_list(cls, v):
        return SkillsList(v)
