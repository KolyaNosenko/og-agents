from rdflib import Graph
from requests import Response

from og_agents.config import AppConfig
from og_agents.ontology.validators.base_ontology_validator import BaseOntologyValidator
from og_agents.ontology.validators.ontology_validation_result import OntologyValidationResult
from og_agents.ontology.validators.oops.oops_validation_result import OOPSValidationResult
from og_agents.common.http_client import HttpClient

REQUEST_BODY_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<OOPSRequest>
    <OntologyUrl></OntologyUrl>
    <OntologyContent>
        <![CDATA[{ontology_data}]]>
    </OntologyContent>
    <Pitfalls>{pitfalls}</Pitfalls>
    <OutputFormat>{output_format}</OutputFormat>
</OOPSRequest>
"""


class OOPSOntologyValidator(BaseOntologyValidator):
    _http_client: HttpClient
    _config: AppConfig

    def __init__(self, http_client: HttpClient, config: AppConfig):
        self._http_client = http_client
        self._config = config

    def validate_ttl(self, ontology_ttl: str) -> OOPSValidationResult:
        rdfxml = self._turtle_to_rdfxml(ontology_ttl)
        result = self._call_oops(rdfxml)

        result = OOPSValidationResult.from_raw_xml(
            result.content,
            self._config.oops_ignored_pitfalls
        )

        return result

    # TODO move to RDF class
    def _turtle_to_rdfxml(self, ontology_ttl: str) -> str:
        g = Graph()

        g.parse(data=ontology_ttl, format="turtle")
        return g.serialize(format="xml")

    def _call_oops(self, ontology_data: str) -> Response:
        body = REQUEST_BODY_TEMPLATE.format(
            ontology_data=ontology_data,
            pitfalls="",
            output_format="XML"
        )
        response = self._http_client.post(
            self._config.oops_api_url,
            data=body.encode("utf-8"),
            headers={"Content-Type": "application/xml; charset=utf-8"},
            # TODO move to env
            timeout=60,
        )

        return response
