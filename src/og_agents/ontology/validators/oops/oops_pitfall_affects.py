from typing import List
from lxml import etree

def get_uris_from_xpath(
        ctx: etree._Element,
        xpath: str,
        namespaces: dict[str, str]
) -> List[str]:
    out: List[str] = []
    for el in ctx.xpath(xpath, namespaces=namespaces):
        txt = (getattr(el, "text", None) or "").strip()
        if txt:
            out.append(txt)
    return out


class OOPSPitfallAffects:
    direct: List[str]
    might_be_equivalent_props: List[str]
    might_be_equivalent_attrs: List[str]
    might_not_be_inversed_of: List[str]

    def __init__(
            self,
            direct: List[str],
            might_be_equivalent_props: List[str],
            might_be_equivalent_attrs: List[str],
            might_not_be_inversed_of: List[str]
    ):
        self.direct = direct
        self.might_be_equivalent_props = might_be_equivalent_props
        self.might_be_equivalent_attrs = might_be_equivalent_attrs
        self.might_not_be_inversed_of = might_not_be_inversed_of

    @staticmethod
    def from_xml_pitfall(
            pitfall_el: etree._Element,
            namespaces: dict[str, str]
    ) -> "OOPSPitfallAffects":
        direct = get_uris_from_xpath(
            pitfall_el,
            "./oops:Affects/oops:AffectedElement",
            namespaces
        )
        might_be_equivalent_props = get_uris_from_xpath(
            pitfall_el,
            "./oops:Affects/oops:MightBeEquivalentProperty/oops:AffectedElement",
            namespaces
        )
        might_be_equivalent_attrs = get_uris_from_xpath(
            pitfall_el,
            "./oops:Affects/oops:MightBeEquivalentAttribute/oops:AffectedElement",
            namespaces
        )
        might_not_be_inversed_of = get_uris_from_xpath(
            pitfall_el,
            "./oops:Affects/oops:MightNotBeInversedOf/oops:AffectedElement",
            namespaces
        )

        return OOPSPitfallAffects(
            direct=direct,
            might_be_equivalent_props=might_be_equivalent_props,
            might_be_equivalent_attrs=might_be_equivalent_attrs,
            might_not_be_inversed_of=might_not_be_inversed_of,
        )
