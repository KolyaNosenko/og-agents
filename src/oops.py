from __future__ import annotations

import requests
from dataclasses import dataclass
from typing import Iterable, Optional

from rdflib import Graph

# OOPS_REST_URL = "https://oops.linkeddata.es/rest"  # public service :contentReference[oaicite:1]{index=1}
OOPS_REST_URL = "http://localhost:80/rest"  # public service :contentReference[oaicite:1]{index=1}



def turtle_to_rdfxml(ttl_text: str) -> str:
    g = Graph()
    g.parse(data=ttl_text, format="turtle")
    return g.serialize(format="xml")  # RDF/XML

@dataclass(frozen=True)
class OOPSPitfall:
    code: str
    name: Optional[str] = None
    description: Optional[str] = None


def scan_with_oops(
    *,
    ontology_rdf_text: str | None = None,
    # ontology_url: str | None = None,
    # pitfalls: Iterable[str | int] | None = None,  # e.g. ["P04","P08"] or [4,8]
    output_format: str = "XML",  # "XML" or "RDF/XML" :contentReference[oaicite:2]{index=2}
    # timeout_s: int = 60,
) -> str:
    rdfxml = turtle_to_rdfxml(ontology_rdf_text)

    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <OOPSRequest>
      <OntologyUrl></OntologyUrl>
      <OntologyContent><![CDATA[
    {rdfxml}
      ]]></OntologyContent>
      <Pitfalls></Pitfalls>
      <OutputFormat>{output_format}</OutputFormat>
    </OOPSRequest>
    """
    r = requests.post(
        OOPS_REST_URL,
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/xml; charset=utf-8"},
        timeout=60,
    )
    r.raise_for_status()
    return r.content.decode("utf-8")


if __name__ == "__main__":
    # Example: scan a local Turtle file by sending its text
    ttl = open("bad_example.ttl", "r", encoding="utf-8").read()
    Graph().parse("bad_example.ttl", format="turtle")
    xml_report = scan_with_oops(ontology_rdf_text=ttl, output_format="XML")
    print("Response:", xml_report)
