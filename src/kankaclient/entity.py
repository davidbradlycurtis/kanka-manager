from dataclasses import dataclass

@dataclass
class Entity:
    id: int
    name: str
    entry: str
    entry_parsed: str
    image: str
    image_full: str
    image_thumb: str
    is_private: str
    tags: list

@dataclass
class Character(Entity):
    title: str
    age: str
    pronouns: str
    type: str
    family_id: int
    location_id: int
    races: list
    is_dead: bool
    image_url: str
    personality_name: list
    personality_entry: list
    appearance_name: list
    appearance_entry: list
    is_personality_visible: bool