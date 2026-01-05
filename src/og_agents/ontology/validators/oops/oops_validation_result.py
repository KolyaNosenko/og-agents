from typing import List, Optional
from lxml import etree

from og_agents.ontology.validators.ontology_validation_result import OntologyValidationResult
from og_agents.ontology.validators.oops.oops_pitfall import OOPSPitfall
from og_agents.ontology.validators.oops.oops_pitfall_affects import OOPSPitfallAffects

def normalize_text(s: Optional[str]) -> str:
    return (s or "").strip()

class OOPSValidationResult(OntologyValidationResult):
    _pitfalls: List[OOPSPitfall]

    def __init__(self, pitfalls: List[OOPSPitfall]):
        super().__init__()
        self._pitfalls = pitfalls

    def is_valid(self) -> bool:
        return len(self._pitfalls) == 0

    @property
    def pitfalls(self) -> List[OOPSPitfall]:
        return self._pitfalls

    @property
    def error_messages(self) -> List[str]:
        messages: List[str] = []
        for p in self._pitfalls:
            # base header line
            header = f"[{p.code}] {p.name} (Importance: {p.importance})"

            # compact affects summary
            affects_bits: List[str] = []
            if p.number_affected is not None:
                affects_bits.append(f"affected: {p.number_affected}")

            if p.affects is not None:
                if p.affects.direct:
                    affects_bits.append(f"direct={len(p.affects.direct)}")
                if p.affects.might_be_equivalent_props:
                    affects_bits.append(f"equiv_props={len(p.affects.might_be_equivalent_props)}")
                if p.affects.might_be_equivalent_attrs:
                    affects_bits.append(f"equiv_attrs={len(p.affects.might_be_equivalent_attrs)}")
                if p.affects.might_not_be_inversed_of:
                    affects_bits.append(f"not_inverse_of={len(p.affects.might_not_be_inversed_of)}")

            if affects_bits:
                messages.append(f"{header} — " + ", ".join(affects_bits))
            else:
                messages.append(header)

        return messages

    @property
    def error_message(self) -> str:
        return "\n\n".join(self.error_messages)

    @staticmethod
    def from_raw_xml(xml: str, ignored_pitfalls: tuple) -> "OOPSValidationResult":
        namespaces = {"oops": "http://www.oeg-upm.net/oops"}

        parser = etree.XMLParser(recover=True, resolve_entities=True, huge_tree=True)
        root = etree.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml, parser=parser)

        pitfalls: List[OOPSPitfall] = []

        for xml_pitfall in root.xpath(".//oops:Pitfall", namespaces=namespaces):
            code = normalize_text(xml_pitfall.findtext("oops:Code", namespaces=namespaces))

            if code in ignored_pitfalls:
                print('Ignoring pitfalls $', code)
                continue

            name = normalize_text(xml_pitfall.findtext("oops:Name", namespaces=namespaces))
            description = normalize_text(xml_pitfall.findtext("oops:Description", namespaces=namespaces))
            importance = normalize_text(xml_pitfall.findtext("oops:Importance", namespaces=namespaces))

            number_affected_text = normalize_text(xml_pitfall.findtext("oops:NumberAffectedElements", namespaces=namespaces))
            number_affected = int(number_affected_text) if number_affected_text.isdigit() else 0

            affects = OOPSPitfallAffects.from_xml_pitfall(xml_pitfall, namespaces)

            pitfalls.append(
                OOPSPitfall(
                    code=code,
                    name=name,
                    description=description,
                    importance=importance,
                    affects=affects,
                    number_affected=number_affected,
                )
            )

        return OOPSValidationResult(pitfalls=pitfalls)
