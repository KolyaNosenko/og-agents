import streamlit as st

st.title("Що хочеш дізнатися?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ставте запитання"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # # Container for assistant message
    # with st.chat_message("assistant"):
    #     context = context_retriever.get_context_from_query(prompt)
    #
    #     prompt_messages = (
    #         PromptBuilder()
    #         .for_answer_generation(context, prompt)
    #         .get_chat_prompt_messages()
    #     )
    #
    #     # Stream model output
    #     def stream_generator():
    #         for chunk in language_model.stream(prompt_messages):
    #             # `chunk.content` accumulates text for chat models
    #             yield chunk.content
    #
    #     full_response = st.write_stream(stream_generator())
    #
    # # Save assistant response
    # st.session_state.messages.append(
    #     {"role": "assistant", "content": full_response}
    # )