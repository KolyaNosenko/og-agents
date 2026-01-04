from dataclasses import dataclass
from typing import Optional

from src.og_agents.ontology.validators.oops.oops_pitfall_affects import OOPSPitfallAffects

@dataclass
class OOPSPitfall:
    code: str
    name: str
    description: str
    importance: str
    affects: OOPSPitfallAffects | None
    number_affected: Optional[int] = None
