from langchain_core.prompts import PromptTemplate

from og_agents.documents import OntologySourceDocument

# PROMPT_TEMPLATE = """
# Your task is to contribute to creating a piece of well-structured ontology by reading information that appeared in the given competency questions, documents and requirements(if there are any).
# The way you approach this is based on provided competency questions and documents related to competency questions. You have to generate RDF ontology so it can answer this competency question. You should read these definitions to understand the concepts:
# Competency questions are a natural language question that specifies the requirements of an ontology and can be answered by that ontology.
# Classes are the keywords/classes that are going to be node types in the knowledge graph ontology. try to extract all classes, in addition, classes are also can be defined for reification. We use Turtle Syntax for representation. Hierarchies are rdfs:subClassOf in the turtle syntax. They can be used to classify similar classes in one superclass. To do this you can find similar nodes and create/use a class as their parent class, for example, adding the node "Employee" is a good middleware and superclass for "Professors" and "Administrator" if provided documents related to ontology of a university. Mostly the lengthier the hierarchy the better. One way can be categorizing classes into several classes and creating superclasses for them. Also keep in mind you can add Equivalent To, General class axioms, Disjoint with, and Disjoint Union of, for each class.
# In your ontology modeling, for each competency question, when faced with complex scenarios that involve more than two entities or a combination of entities and datatypes, apply reification. Specifically, create a pivot class to act as an intermediary for these entities, ensuring the nuanced relationships are accurately captured. For instance, when representing "a user accessed a resource at a given time", establish a pivot class like UserResourceUsage, linked from the user, resource, and the specific time of access to UserResourceInteraction, rather than directly connecting the user to both the resource and time.
# Then you need to create properties (owl:Property). In this step, you use classes from the previous stage and create object and data properties to connect them and establish the ontology. Always output a turtle syntax, if you need more classes to model a competency question between more than 2 concepts, feel free to add more pivot (reification) classes here. try to find as much relation as possible by reading competency questions and documents. At this stage, you can create both data and object properties. Data properties are between classes or hierarchy classes and data types such as xsd:string, xsd:integer, xsd:decimal, xsd:dateTime, xsd:date, xsd:time, xsd:boolean, xsd:byte, xsd:double, xsd:float and etc. For example, in the university domain, we have: employee_id a owl:Property ; rdfs:domain :Teacher ; rdfs:range xsd:integer. Object properties are between classes. try to find as much relation as possible by reading competency questions and the story. Feel free to use rdfs:subPropertyOf for creating hierarchies for relations. For modeling properties (object or data properties) if it is necessary, use these relations characteristics: Functional, Inverse functional, Transitive, Symmetric, Asymmetric, Reflexive, and Irreflexive. Also, you are flexible in domain and range so you can use Class1 or Class2 in domain and range or disjoint with, the inverse of between relations.
# It is common to forget to add relations that are related to reification: In RDF reification, achieving precise modeling is pivotal, especially when handling multifaceted scenarios where mere binary associations fall short. Take for instance the statement, "a user used a resource at a time". While it might initially seem to involve a direct link between a 'User' and a 'Resource', it inherently embodies three entities: a 'User', a 'Resource', and a 'Time'. Directly connecting 'User' to both 'Resource' and 'Time' fails to capture the essence of the statement, as it obscures which resource was utilized by the user at a specific time. To address this, a more sophisticated modeling approach is needed, invoking a pivot class, UsingResource. This pivot class acts as an intermediary, linking both User and Resource. Furthermore, it integrates a time property to denote the exact instance of usage. By employing this method, we can coherently model the statement, ensuring that the user's interaction with a specific resource at a distinct time is unambiguously represented. This approach highlights the imperative of ontology design patterns and the necessity of intermediary nodes when modeling complex relationships involving multiple entities or a mix of entities and datatypes.
# Upon implementation of restrictions, feel free to use owl:equivalentClass [ rdf:type owl:Restriction ;  owl:onProperty :{{relation}} ;  owl:allValuesFrom :{{Class}} ] ; in this way, you can put restrictions for classes such as class Class1 is the only class that uses the relation R. or you can put soft restrictions by using owl:someValuesFrom. Also, you can use general class axioms: [ rdf:type owl:Restriction ; owl:onProperty :R1 ; owl:someValuesFrom :Class1 ; rdfs:subClassOf :Class2 ] when you want to put restrictions on the definition of a class based on its relation and the definition is necessary but not enough (if it is enough it would be equivalent to owl:equivalentClass).
#
# These are the prefixes:
# @prefix : <http://www.example.org/test#> .
# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
# @prefix owl: <http://www.w3.org/2002/07/owl#>.
#
# Important:
# Return ONLY the final RDF, without any additional text.
# Bind all resources added to the ontology to the ":" prefix.
#
# Documents: {documents}
#
# Competency questions:
# {competency_questions}
#
# Tip:
# Here are some possible mistakes that you might make:
# 1- forgetting to add prefixes at the beginning of the code.
# 2- forgetting to write pivot classes at the beginning before starting to code.
# 3- you usually forget to write the name of the reification (pivot) that you want to create at the beginning of the output
# 4- In reification, the reification node (pivot class) is connected to all related classes by object properties, not by the subclassof. it can be a subclass of something, but for reification, it needs object properties.
# common mistakes in extracting classes:
# 1- Mistake: not extracting all classes and missing many of them. classes can be found in the documents, or in the competency questions.
# 2- Returning empty answer
# 3- Providing comments or explanations
# 4- Extracting classes like 'Date', and 'integer' are wrong since they are data properties.
# 5- Not using RDF reification: not extracting pivot classes for modeling relation between classes (more than one class and one data property, or more than two classes)
# 6- Extracting individuals in the text as a class
# 7- The pivot class is not a subclass of its components.
# common mistakes in the hierarchy extraction:
# 1- creating an ontology for non-existing classes: creating a new leaf and expanding it into the root
# 2- returning empty answer or very short
# 3- Providing comments or explanations
# 4- Extracting attributes such as date, time, and string names that are related to data properties
# 5- Forget to add "" around the strings in the tuples
# Common mistakes in the object_properties:
# 1- returning new variables with anything except object_properties
# 2- returning empty answer or very short
# 3- providing comments or explanations
# 4- when the pivot class is created, all of the related classes should point to it (direction of relation is from the classes (domains) 'to'  pivot class (range))
# Common mistakes in the data_properties:
# 1- returning new variables with anything except data_properties
# 2- returning empty answer or very short
# 3- providing comments or explanations
# """

PROMPT_TEMPLATE = """
Твоє завдання — зробити внесок у створення добре структурованої онтології, прочитавши інформацію, що міститься в наданих документах, вимогах та обмеженнях (якщо вони є).
Для вирішення цієї задачі бери кожне competency question (компетентнісне питання) по черзі. Далі згенеруйте RDF так, щоб онтологія могла відповідати на це competency question. Ваш результат має бути валідною онтологією у RDF, яка може відповісти на всі надані питання компетентності.
Прочитай ці визначення, щоб краще розібратися з поняттями:
Питання компетентності — це питання природною мовою, які задають вимоги до онтології та на які ця онтологія повинна вміти відповідати.
Класи (Classes) — це ключові слова/класи, які стануть типами вузлів (node types) в графі знань онтології. Спробуй видобути всі класи; окрім того, класи можуть бути створені для реїфікації (reification).
Для представлення онтології використовуй синтаксис Turtle.
Ієрархії задаються через rdfs:subClassOf у Turtle-синтаксисі. Їх можна використовувати, щоб класифікувати подібні класи під одним суперкласом. Для цього ви можете знаходити схожі вузли й створювати/використовувати клас як їхнього батька. Наприклад, додавання вузла "Клас_Працівник" є хорошим проміжним рівнем і суперкласом для "Клас_Професор" та "Клас_Адміністратор", якщо спираючись на документи необхідно моделювати онтологію університету. Зазвичай глибша ієрархія — краще. Один зі способів — категоризувати класи у кілька груп і створювати для них суперкласи. Важливо: імена класів мають префікс Клас_, наприклад Клас_Професор. Також май на увазі, що для кожного класу можна додавати Equivalent To (еквівалентність), загальні аксіоми класів (General class axioms), Disjoint with (несумісність), та Disjoint Union of (диз’юнктне об’єднання).
У моделюванні онтології для кожного питання компетентності, коли стикаєшся зі складними сценаріями, що включають більше ніж дві сутності або комбінацію сутностей і типів даних (datatypes), застосовуй реїфікацію. Тобто створюй pivot class (проміжний клас) як посередника між цими сутностями, щоб коректно відобразити нюансні відношення. Наприклад, для «користувач отримав доступ до ресурсу в певний час» створіть pivot class на кшталт Клас_КористувачВикориставРесурс, пов’язану з користувачем, ресурсом та конкретним часом доступу через Клас_ВзаємодіяКористувачаЗРесурсом, замість того щоб напряму з’єднувати користувача одночасно з ресурсом і часом.
Далі тобі потрібно створити властивості (owl:Property). На цьому кроці використовуй класи з попереднього етапу й створюй об’єктні (object) та дататипні (data) властивості, щоб з’єднати їх і сформувати онтологію. Завжди виводь Turtle-синтаксис. Якщо для моделювання питання компетентності між більш ніж 2 поняттями потрібні додаткові класи — сміливо додавай більше pivot класів (класів для реїфікації). Намагайся знайти якнайбільше зв’язків, читаючи питання компетентності, документи та обмеження. На цьому етапі можеш створювати і data, і object properties.
Data properties — між класами (або класами в ієрархії) та типами даних, такими як xsd:string, xsd:integer, xsd:decimal, xsd:dateTime, xsd:date, xsd:time, xsd:boolean, xsd:byte, xsd:double, xsd:float тощо. Наприклад, у домені університету: вік a owl:Property ; rdfs:domain :Вчитель ; rdfs:range xsd:integer.
Object properties — між класами. Намагайся знайти якнайбільше зв’язків, читаючи питання компетентності і документи. Можеш використовувати rdfs:subPropertyOf для створення ієрархій відношень. Для моделювання властивостей (object або data) за потреби використовуй характеристики відношень: Functional, Inverse functional, Transitive, Symmetric, Asymmetric, Reflexive, Irreflexive. Також гнучко задавай domain і range: можеш ставити у domain/range Клас_клас1 або Клас_клас2, або використовувати disjoint with, або інверсію між відношеннями.
Часто забувають додати відношення, пов’язані з реїфікацією: у RDF реїфікації точне моделювання є ключовим, особливо коли потрібно обробляти багатокомпонентні сценарії, де простих бінарних зв’язків недостатньо. Наприклад, твердження «користувач використав ресурс у певний час». Хоча на перший погляд воно виглядає як прямий зв’язок між «користувачем» і «ресурсом», насправді воно містить три сутності: «користувач», «ресурс» і «час». Пряме з’єднання «користувача» одночасно з «ресурсом» і «часом» не передає суті, бо неясно, який саме ресурс було використано користувачем у конкретний час. Щоб це виправити, потрібен складніший підхід: pivot class, наприклад Клас_ВикористанняРесурсу. Цей pivot class виступає посередником, з’єднуючи Клас_Користувач і Клас_Ресурс. Крім того, він включає властивість часу, щоб зафіксувати точний момент використання. Застосовуючи цей метод, можна узгоджено змоделювати твердження, гарантуючи однозначне представлення взаємодії користувача з конкретним ресурсом у конкретний час. Це підкреслює важливість патернів проєктування онтологій і потребу в проміжних вузлах при моделюванні складних зв’язків, що включають кілька сутностей або суміш сутностей і типів даних.
Під час застосування обмежень (restrictions) можеш використовувати:
owl:equivalentClass [ rdf:type owl:Restriction ; owl:onProperty :{{relation}} ; owl:allValuesFrom :{{Class}} ] ;
так ти можеш задавати обмеження для класів, наприклад «клас Клас_клас1 — єдиний клас, що використовує відношення Відношення1». Або можете задавати «м’якші» обмеження через owl:someValuesFrom. Також можна використовувати загальні аксіоми класів:
[ rdf:type owl:Restriction ; owl:onProperty :Відношення1 ; owl:someValuesFrom :Клас_клас1 ; rdfs:subClassOf :Клас_клас2 ]
коли ти хочеш накласти обмеження на визначення класу на основі його відношення, і це визначення є необхідним, але недостатнім (якщо достатнє — тоді це було б еквівалентно owl:equivalentClass).

Ось префікси:
@prefix : [http://www.example.org/test#](http://www.example.org/test#) .
@prefix rdf: [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns#) .
@prefix rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#) .
@prefix xsd: [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema#) .
@prefix owl: [http://www.w3.org/2002/07/owl#](http://www.w3.org/2002/07/owl#) .

Важливо:
1. Поверни ЛИШЕ фінальний RDF, без будь-якого іншого тексту.
2. Прив’яжи усі ресурси, що додаються до онтології, до префікса ":".
3. Користуйся типами xsd.
4. Не використовуй langString

Документи: {documents}

Питання компетентності:
{competency_questions}

Порада:
Ось типові помилки, яких можна припустити:
1. забути додати префікси на початку коду;
2. забути виписати pivot-класи на початку;
3. ваш вивід може бути приєднаний до попереднього RDF-виводу, тому не пишіть повторювані слова, класи тощо;
4. зазвичай забувають написати назву реїфікації (pivot), яку хочеш створити, на початку виводу;
5. у реїфікації вузол реїфікації (pivot class) з’єднується з усіма пов’язаними класами через object properties, а не через subClassOf. Він може бути підкласом чогось, але для реїфікації йому потрібні object properties.

Типові помилки при витягуванні класів:
1. помилка: не витягнути всі класи й пропустити багато з них (класи можна знайти в документах, або питанні компетентності, або в обмеженнях);
2. повернути порожню відповідь;
3. додавати коментарі або пояснення;
4. витягувати атрибути на кшталт 'Date' або 'integer' як класи — неправильно, бо це data properties;
5. не використовувати RDF-реїфікацію: не витягувати pivot-класи для моделювання відношення між класами (більше ніж один клас і одна data property, або більше ніж два класи);
6. витягувати індивідів із тексту як клас;
7. pivot class не є підкласом своїх компонентів.

Типові помилки у витягуванні ієрархії:
1. створювати онтологію для неіснуючих класів: створювати новий «листок» і розгортати його до кореня;
2. повертати порожню або дуже коротку відповідь;
3. додавати коментарі або пояснення;
4. витягувати атрибути типу date, time, string names, які належать до data properties;
5. забувати ставити "" навколо рядків у кортежах.

Типові помилки в object_properties:
1. повертати нові змінні з чимось, окрім object_properties;
2. повертати порожню або дуже коротку відповідь;
3. додавати коментарі або пояснення;
4. коли створено pivot class, усі пов’язані класи мають вказувати на нього (напрямок зв’язку: від класів (domain) «до» pivot class (range)).

Типові помилки в data_properties:
1. повертати нові змінні з чимось, окрім data_properties;
2. повертати порожню або дуже коротку відповідь;
3. додавати коментарі або пояснення.
"""

class GenerateOntologyPrompt:
    _template: PromptTemplate

    def __init__(self):
        self._template = PromptTemplate.from_template(PROMPT_TEMPLATE)

    def format(
            self,
            competency_questions: str,
            documents: list[OntologySourceDocument]
    ) -> str:
        formatted_documents = []

        for index, document in enumerate(documents):
            formatted_documents.append(document.to_prompt_format(index))

        joined_documents = '\n'.join(formatted_documents)

        return self._template.format(competency_questions=competency_questions, documents=joined_documents)