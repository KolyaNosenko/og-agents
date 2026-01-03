from src.og_agents.config import AppConfig
from src.og_agents.documents import OntologySourceDocument
from src.og_agents.language_models import OpenAILanguageModel
from src.og_agents.workflows import OntologyGenerationWorkflowBuilder, WorkflowContext

def main():
    config = AppConfig.init()

    workflow = OntologyGenerationWorkflowBuilder.create(config).build()
    language_model = OpenAILanguageModel.create(config)

    # TODO add metadata
    # TODO add structured output
    workflow.invoke(
        {
            'documents': [
                OntologySourceDocument(
                    page_content="В тихому мальовничому селищі, яке притулилося одним боком до лісу, а другим до огорожі місцевої птахофабрики та невеличкого клаптика поля, жила сім’я Петренків. Сім’я складалася з батька Семена Петровича, матері Олени Степанівни та двох доньок Іринки та Яни. Сім’я була звичайна, як більшість українських сімей. Діти ходили до школи. Іринка була старша і вчилася уже в сьомому класі, а Яна була меншою в сім’ї і вчилася у третьому класі селищної школи десятирічки. Загалом у школі навчалося 82 учні, серед яких 42 учні навчалися у початкових класах, а решта - у старших класах. Учителів у школі було не багато і тому деякі учителі викладали по декілька предметів у різних класах. Зокрема математику і фізику викладала Марія Петрівна, біологію і хімію – Петро Іванович, Степан Іванович – фізкультуру та військову справу. Стеха Романівна – природознавство, екологію, Семен Петрович - працю та народознавство, Петро Юрійович – історію, Микола Миколайович – українську та зарубіжну літературу, решта вчителів викладали домоводство, етику, психологію, співи. Всього у школі працювало 11 учителів, які забезпечували навчально-виховний процес."
                ),
            ]
        },
        context=WorkflowContext(language_model=language_model)
    )

if __name__ == "__main__":
    main()