import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("제주도 여행 정보 챗봇")
st.write(
    "제주도 여행 정보를 제공하는 챗봇 서비스입니다."
    "이 앱을 사용하려면 OpenAI API 키가 필요하며,"
    "제주도 여행에 대한 유용한 팁과 정보를 원하시면, 언제든지 질문해 주세요!"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("OpenAI API key를 입력해야 서비스가 됩니다.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("제주도 여행 관련 질문을 입력해 주세요?"):

    # 사용자 입력 받기
    # st.write("궁금한 제주도 여행 정보를 입력하세요!")
    # if prompt := st.chat_input("여행 관련 질문을 입력해 주세요:", ""):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4.0-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
