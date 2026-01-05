from og_agents.common.http_client import RequestsHttpClient
from og_agents.config import AppConfig
from og_agents.documents import OntologySourceDocument
from og_agents.language_models import OpenAILanguageModel
from og_agents.ontology import OntologyStorage
from og_agents.workflows import OntologyGenerationWorkflowBuilder, WorkflowContext


def main():
    config = AppConfig.init()
    http_client = RequestsHttpClient()

    workflow = OntologyGenerationWorkflowBuilder.create(config).build()
    language_model = OpenAILanguageModel.create(config)
    ontology_storage = OntologyStorage(config)

    ttl = """
@prefix : <http://www.example.org/test#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:Family a owl:Class .
:Person a owl:Class .
:School a owl:Class .
:GeographicFeature a owl:Class .
:Village a owl:Class .
:Role a owl:Class .
:FamilyMember a owl:Class .

:attendsSchool a owl:ObjectProperty ;
  rdfs:domain :Person ;
  rdfs:range :School .

:grade a owl:DatatypeProperty ;
  rdfs:domain :Person ;
  rdfs:range xsd:string .

:tenYearSystem a owl:DatatypeProperty ;
  rdfs:domain :School ;
  rdfs:range xsd:boolean .

:totalStudents a owl:DatatypeProperty ;
  rdfs:domain :School ;
  rdfs:range xsd:integer .

:primaryClassCount a owl:DatatypeProperty ;
  rdfs:domain :School ;
  rdfs:range xsd:integer .

:seniorClassCount a owl:DatatypeProperty ;
  rdfs:domain :School ;
  rdfs:range xsd:integer .

:numOfMembers a owl:DatatypeProperty ;
  rdfs:domain :Family ;
  rdfs:range xsd:integer .

:homeLocation a owl:ObjectProperty ;
  rdfs:domain :Family ;
  rdfs:range :Village .

:adjacentTo a owl:ObjectProperty ;
  rdfs:domain :Village ;
  rdfs:range :GeographicFeature .

:hasFamilyMember a owl:ObjectProperty ;
  rdfs:domain :Family ;
  rdfs:range :FamilyMember .

:familyMemberPerson a owl:ObjectProperty ;
  rdfs:domain :FamilyMember ;
  rdfs:range :Person .

:familyMemberRole a owl:ObjectProperty ;
  rdfs:domain :FamilyMember ;
  rdfs:range :Role .

:familyMemberOf a owl:ObjectProperty ;
  rdfs:domain :FamilyMember ;
  rdfs:range :Family .

:name a owl:DatatypeProperty ;
  rdfs:domain :Person, :School, :Village, :GeographicFeature ;
  rdfs:range xsd:string .

:Forest a :GeographicFeature .
:PoultryFarmFence a :GeographicFeature .
:Field a :GeographicFeature .

:PetrenkoVillage a :Village ;
  :name "Petrenko Village" .

:PetrenkoSchool a :School ;
  :name "Petrenko School" ;
  :tenYearSystem "true"^^xsd:boolean ;
  :totalStudents "82"^^xsd:integer ;
  :primaryClassCount "42"^^xsd:integer ;
  :seniorClassCount "40"^^xsd:integer .

:SemenPetrovich a :Person ;
  :name "Semen Petrovich" .

:OlenaStepanivna a :Person ;
  :name "Olena Stepanivna" .

:IrinkaPetrenko a :Person ;
  :name "Irinka Petrenko" ;
  :grade "7" ;
  :attendsSchool :PetrenkoSchool .

:YanaPetrenko a :Person ;
  :name "Yana Petrenko" ;
  :grade "3" ;
  :attendsSchool :PetrenkoSchool .

:FatherRole a :Role .
:MotherRole a :Role .
:DaughterRole a :Role .

:PetrenkoFatherMember a :FamilyMember ;
  :familyMemberPerson :SemenPetrovich ;
  :familyMemberRole :FatherRole ;
  :familyMemberOf :PetrenkoFamily .

:PetrenkoMotherMember a :FamilyMember ;
  :familyMemberPerson :OlenaStepanivna ;
  :familyMemberRole :MotherRole ;
  :familyMemberOf :PetrenkoFamily .

:PetrenkoDaughter1Member a :FamilyMember ;
  :familyMemberPerson :IrinkaPetrenko ;
  :familyMemberRole :DaughterRole ;
  :familyMemberOf :PetrenkoFamily .

:PetrenkoDaughter2Member a :FamilyMember ;
  :familyMemberPerson :YanaPetrenko ;
  :familyMemberRole :DaughterRole ;
  :familyMemberOf :PetrenkoFamily .

:PetrenkoFamily a :Family ;
  :numOfMembers "4"^^xsd:integer ;
  :homeLocation :PetrenkoVillage ;
  :hasFamilyMember :PetrenkoFatherMember , :PetrenkoMotherMember , :PetrenkoDaughter1Member , :PetrenkoDaughter2Member ;
  :isTypicalFamily "true"^^xsd:boolean .

:Forest :GeographicFeature ;
  :name "Forest" .

:PoultryFarmFence :GeographicFeature ;
  :name "Fence of Poultry Farm" .

:Field :GeographicFeature ;
  :name "Patch of Field" .

:PetrenkoVillage :Village ;
  :name "Petrenko Village" ;
  :adjacentTo :Forest , :PoultryFarmFence , :Field .

:PetrenkoSchool :School ;
  :name "Petrenko School" .
    """


    # consistency_validator = OntologyConsistencyValidator()
    #
    # response = consistency_validator.validate_ttl(ttl)
    #
    # print(response.error_message)

    # if not response.is_valid():
    #     prompt = OntologyConsistencyValidationResultPrompt().format(ontology_ttl=ttl, validation_result=response)
    #     print(prompt)
    #
    #     result = language_model.invoke(prompt)
    #     ontology_ttl = result.content
    #
    #     print("Ontology generated:", ontology_ttl)

    # rdf_validator = OntologyRDFSyntaxValidator()
    # result = rdf_validator.validate_ttl(ttl)
    #
    # if not result.is_valid():
    #     print('Not valid!!')
    #     prompt = OntologyConsistencyValidationResultPrompt().format(ontology_ttl=ttl, validation_result=result)
    #
    #     print('PROMOPT!', prompt)
    #
    # if result.is_valid():
    #     print('Valid!!')


    # TODO add metadata
    # TODO add structured output
    workflow.invoke(
        {
            'documents': [
                OntologySourceDocument(
                    page_content="В тихому мальовничому селищі, яке притулилося одним боком до лісу, а другим до огорожі місцевої птахофабрики та невеличкого клаптика поля, жила сім’я Петренків. Сім’я складалася з батька Семена Петровича, матері Олени Степанівни та двох доньок Іринки та Яни. Сім’я була звичайна, як більшість українських сімей. Діти ходили до школи. Іринка була старша і вчилася уже в сьомому класі, а Яна була меншою в сім’ї і вчилася у третьому класі селищної школи десятирічки. Загалом у школі навчалося 82 учні, серед яких 42 учні навчалися у початкових класах, а решта - у старших класах."
                    # page_content="""
                    # **The Topps Company, Inc.** is an American company that manufactures trading cards and other collectibles. Formerly based in New York City, Topps is best known as a leading producer of baseball and other sports and non-sports themed trading cards. Topps also produces cards under the brand names Allen & Ginter and Bowman.
                    # In the 2010s, Topps was the only baseball card manufacturer with a license with Major League Baseball. Following the loss of that license to Fanatics, Inc. in 2022, Fanatics acquired Topps in the same year.
                    # """
                ),
            ]
        },
        context=WorkflowContext(
            config=config,
            http_client=http_client,
            language_model=language_model,
            ontology_storage=ontology_storage
        )
    )

if __name__ == "__main__":
    main()