from owlready2 import World
from rdflib import Graph
from og_agents.config import AppConfig
from io import BytesIO

class OntologyStorage:
    _config: AppConfig
    _world: World

    def __init__(self, config: AppConfig):
        self._config = config

        world = World()
        world.set_backend(filename=self._config.db.file_path, backend="sqlite")
        self._world = world

    def create_from_ttl(self, ontology_ttl: str):
        rdf_graph = Graph()
        rdf_graph.parse(data=ontology_ttl, format="turtle")

        rdfxml_bytes = rdf_graph.serialize(format="xml")

        if isinstance(rdfxml_bytes, str):
            rdfxml_bytes = rdfxml_bytes.encode("utf-8")

        onto = self._world.get_ontology(self._config.ontology_name)

        onto.load(fileobj=BytesIO(rdfxml_bytes))

        self._world.save()
        print('Ontology saved to', self._config.db.file_path)

    def load(self):
        return self._world.get_ontology(self._config.ontology_name)

    def get_world_as_rdf_graph(self):
        return self._world.as_rdflib_graph()

    def destroy(self):
        onto = self.load()
        onto.destroy()

        self._world.save()

    def is_exist(self):
        onto = self.load()

        return (
            next(onto.classes(), None) is not None or
            next(onto.object_properties(), None) is not None or
            next(onto.data_properties(), None) is not None or
            next(onto.individuals(), None) is not None
        )
