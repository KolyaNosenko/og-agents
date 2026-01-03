from datetime import datetime
from pathlib import Path
from rdflib import Graph

class OntologyFileManager:
    # TODO add source metadata to filename
    @staticmethod
    def save_ttl(ontology_ttl: str):
        root = Path(__file__).resolve().parents[1]
        static = root / "static"
        static.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ontology_{timestamp}.ttl"
        path = static / filename

        graph = Graph()
        # TODO move validation
        graph.parse(data=ontology_ttl, format="turtle")
        graph.serialize(path, format="turtle")