from typing import Dict, List, Set
from dataclasses import dataclass

from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL
from pyvis.network import Network


OWL_COLORS = {
    "Class": {"background": "#AACCFF", "border": "#5588CC"},
    "ObjectProperty": {"background": "#FFB347", "border": "#CC7A00"},
    "DatatypeProperty": {"background": "#8FBC8F", "border": "#4F8F4F"},
    "AnnotationProperty": {"background": "#D7BDE2", "border": "#8E44AD"},
    "Individual": {"background": "#B0B0B0", "border": "#707070"},
    "Literal": {"background": "#E8F5E9", "border": "#A5D6A7"},
    "BlankNode": {"background": "rgba(160,160,160,0.35)", "border": "#999999"},
    "Ontology": {"background": "#F7DC6F", "border": "#B7950B"},
    "Resource": {"background": "#E0E0E0", "border": "#9E9E9E"},
}

# -----------------------------
# Data models
# -----------------------------

@dataclass(frozen=True)
class Edge:
    s: str
    p: str
    o: str


# -----------------------------
# Constants
# -----------------------------

SCHEMA_PREDS = {
    str(RDFS.subClassOf),
    str(RDFS.domain),
    str(RDFS.range),
    str(RDF.type),
    str(OWL.equivalentClass),
    str(OWL.disjointWith),
    str(OWL.inverseOf),
}

RDF_TYPE = str(RDF.type)
OWL_RDFS_CLASS_URIS = {OWL.Class, RDFS.Class}


# -----------------------------
# Helpers
# -----------------------------

def node_id(n) -> str:
    if isinstance(n, BNode):
        return f"bnode:{str(n)}"
    return str(n)


def shorten(uri: str) -> str:
    if uri.startswith("bnode:"):
        return uri
    if uri.startswith("lit:"):
        return uri[4:]
    if "#" in uri:
        return uri.rsplit("#", 1)[-1]
    if "/" in uri:
        return uri.rstrip("/").rsplit("/", 1)[-1]
    return uri


def node_kind(g: Graph, n) -> str:
    if isinstance(n, Literal):
        return "Literal"
    if isinstance(n, BNode):
        return "BlankNode"
    if not isinstance(n, URIRef):
        return "Resource"

    # explicit typing first
    if (n, RDF.type, OWL.Ontology) in g:
        return "Ontology"
    if (n, RDF.type, OWL.Class) in g or (n, RDF.type, RDFS.Class) in g:
        return "Class"
    if (n, RDF.type, OWL.ObjectProperty) in g:
        return "ObjectProperty"
    if (n, RDF.type, OWL.DatatypeProperty) in g:
        return "DatatypeProperty"
    if (n, RDF.type, OWL.AnnotationProperty) in g:
        return "AnnotationProperty"
    if (n, RDF.type, OWL.NamedIndividual) in g:
        return "Individual"

    # heuristics (schema participation)
    if (n, RDFS.subClassOf, None) in g or (None, RDFS.subClassOf, n) in g:
        return "Class"
    if (n, RDFS.domain, None) in g or (n, RDFS.range, None) in g or (n, OWL.inverseOf, None) in g:
        return "Property"

    return "Resource"



def predicate_kind(g: Graph, p: URIRef, cache: Dict[str, str]) -> str:
    """
    Determine predicate category. Many ontologies don't type predicates,
    so we keep a fallback 'UnknownProperty'.
    """
    pid = str(p)
    if pid in cache:
        return cache[pid]

    if (p, RDF.type, OWL.ObjectProperty) in g:
        cache[pid] = "ObjectProperty"
    elif (p, RDF.type, OWL.DatatypeProperty) in g:
        cache[pid] = "DatatypeProperty"
    elif (p, RDF.type, OWL.AnnotationProperty) in g:
        cache[pid] = "AnnotationProperty"
    elif (p, RDF.type, RDF.Property) in g:
        cache[pid] = "Property"
    else:
        cache[pid] = "UnknownProperty"
    return cache[pid]


def node_style(kind: str) -> Dict:
    color = OWL_COLORS.get(kind, OWL_COLORS["Resource"])
    style: Dict = {"color": color}

    if kind == "Class":
        style.update(shape="ellipse", size=22)
    elif kind in {"ObjectProperty", "DatatypeProperty", "AnnotationProperty"}:
        style.update(shape="diamond", size=16)
    elif kind == "Individual":
        style.update(shape="dot", size=14)
    elif kind == "Literal":
        style.update(shape="box", size=10)
    elif kind == "BlankNode":
        style.update(shape="dot", size=8, opacity=0.6)
    elif kind == "Ontology":
        style.update(shape="hexagon", size=26)
    else:
        style.update(shape="dot", size=12)

    return style


def build_title(g: Graph, term: URIRef, kind: str, *, include_labels: bool, include_comments: bool) -> str:
    parts = [f"{shorten(str(term))} ({kind})", str(term)]

    if include_labels:
        for _, _, lbl in g.triples((term, RDFS.label, None)):
            parts.append(f"label: {lbl}")

    if include_comments:
        for _, _, c in g.triples((term, RDFS.comment, None)):
            parts.append(f"comment: {c}")

    return "\n".join(parts)


# -----------------------------
# Extraction logic (FIXED FILTERS)
# -----------------------------

def extract_edges(
    g: Graph,
    *,
    limit: int,
    show_schema_only: bool,
    show_classes: bool,
    show_object_props: bool,
    show_data_props: bool,
    show_individuals: bool,
) -> List[Edge]:
    """
    Correct filtering:
    - schema_only keeps only schema predicates and respects show_* toggles
    - non-schema filters edges by:
        * literal-object edges -> treated as datatype-ish (controlled by show_data_props)
        * object edges -> filtered using predicate typing when available + node kind filters
    """
    edges: List[Edge] = []
    pred_cache: Dict[str, str] = {}
    kind_cache: Dict[str, str] = {}

    def cached_kind(term) -> str:
        tid = node_id(term)
        if tid in kind_cache:
            return kind_cache[tid]
        k = node_kind(g, term)
        kind_cache[tid] = k
        return k

    def allow_node_kind(k: str) -> bool:
        if k == "Class":
            return show_classes
        if k == "Individual":
            return show_individuals
        # BlankNode/Literal/Resource are allowed if the edge that introduces them is allowed.
        return True

    def allow_schema_edge(p_str: str, p: URIRef, o) -> bool:
        if p_str not in SCHEMA_PREDS:
            return False

        # If classes are hidden, remove class-class schema edges
        if not show_classes and p_str in {str(RDFS.subClassOf), str(OWL.equivalentClass), str(OWL.disjointWith)}:
            return False

        # domain/range/inverseOf are property-schema edges => respect property toggles
        if p_str in {str(RDFS.domain), str(RDFS.range), str(OWL.inverseOf)}:
            pk = predicate_kind(g, p, pred_cache)
            if pk == "ObjectProperty" and not show_object_props:
                return False
            if pk == "DatatypeProperty" and not show_data_props:
                return False
            # UnknownProperty: keep (can be made stricter later)
            return True

        # rdf:type schema filter: only keep the "schema typing" that user wants
        if p_str == RDF_TYPE:
            if o in OWL_RDFS_CLASS_URIS and not show_classes:
                return False
            if o == OWL.ObjectProperty and not show_object_props:
                return False
            if o == OWL.DatatypeProperty and not show_data_props:
                return False
            if o == OWL.NamedIndividual and not show_individuals:
                return False

        return True

    def allow_instance_edge(s, p: URIRef, o) -> bool:
        p_str = str(p)

        # Literal edges -> treat as DatatypeProperty-ish (even if predicate isn't typed)
        if isinstance(o, Literal):
            return show_data_props

        # Non-literal edge: if predicate typed, respect property toggles
        pk = predicate_kind(g, p, pred_cache)
        if pk == "ObjectProperty" and not show_object_props:
            return False
        if pk == "DatatypeProperty" and not show_data_props:
            return False
        # Annotation properties often point to literals; if they point to URI, keep unless you want a toggle later.

        # Node kind filters (classes/individuals)
        sk = cached_kind(s)
        ok = cached_kind(o)
        if not allow_node_kind(sk):
            return False
        if not allow_node_kind(ok):
            return False

        # rdf:type instance filtering: allow types according to toggles
        if p_str == RDF_TYPE:
            # subject is being typed -> decide based on object (class-ish / NamedIndividual marker)
            if o in OWL_RDFS_CLASS_URIS and not show_classes:
                return False
            if o == OWL.NamedIndividual and not show_individuals:
                return False

        return True

    for s, p, o in g:
        if len(edges) >= limit:
            break

        p_str = str(p)

        if show_schema_only:
            if not allow_schema_edge(p_str, p, o):
                continue
        else:
            if not allow_instance_edge(s, p, o):
                continue

        s_id = node_id(s)
        p_id = p_str
        o_id = f'lit:"{o}"' if isinstance(o, Literal) else node_id(o)

        edges.append(Edge(s=s_id, p=p_id, o=o_id))

    return edges


# -----------------------------
# Visualization
# -----------------------------

def visualize_ontology(
    rdf_graph: Graph,
    *,
    height: int = 700,
    limit: int = 200,
    show_classes: bool = True,
    show_object_props: bool = True,
    show_data_props: bool = False,
    show_individuals: bool = False,
    show_schema_only: bool = False,
    show_labels: bool = True,
    show_comments: bool = False,
    physics: bool = True,
    initial_zoom: float = 0.8,
) -> Network:
    """
    Build interactive ontology visualization using PyVis.
    Filters are applied at edge level (not only rdf:type), so show_* toggles work correctly.
    """

    edges = extract_edges(
        rdf_graph,
        limit=limit,
        show_schema_only=show_schema_only,
        show_classes=show_classes,
        show_object_props=show_object_props,
        show_data_props=show_data_props,
        show_individuals=show_individuals,
    )

    net = Network(
        height=f"{height}px",
        width="100%",
        directed=True,
        cdn_resources="in_line",
        select_menu=False,
        filter_menu=False,
    )

    net.toggle_physics(physics)
    net.toggle_drag_nodes(True)
    net.toggle_hide_edges_on_drag(False)
    net.toggle_hide_nodes_on_drag(False)
    net.force_atlas_2based()

    added: Set[str] = set()

    def add_node(node_str: str):
        if node_str in added:
            return

        # Blank nodes (reified relations)
        if node_str.startswith("bnode:"):
            net.add_node(
                node_str,
                label="" if not show_labels else "",  # keep blank by design
                title="Blank node (reified relation)",
                group="BlankNode",
                **node_style("BlankNode"),
            )
            added.add(node_str)
            return

        # Literals
        if node_str.startswith("lit:"):
            net.add_node(
                node_str,
                label=shorten(node_str) if show_labels else "",
                title=shorten(node_str),
                group="Literal",
                **node_style("Literal"),
            )
            added.add(node_str)
            return

        # URI resources
        term = URIRef(node_str)
        kind = node_kind(rdf_graph, term)
        style = node_style(kind)

        title = build_title(
            rdf_graph,
            term,
            kind,
            include_labels=True,          # labels are almost always useful in hover
            include_comments=show_comments,
        )

        net.add_node(
            node_str,
            label=shorten(node_str) if show_labels else "",
            title=title,
            group=kind,
            **style,
        )
        added.add(node_str)

    for e in edges:
        add_node(e.s)
        add_node(e.o)
        net.add_edge(
            e.s,
            e.o,
            label=shorten(e.p) if show_labels else "",
            title=e.p,
            arrows="to",
        )

    return net
