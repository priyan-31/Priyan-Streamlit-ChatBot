import PyPDF2
import streamlit as st
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="PDF Chatbot")

st.title("Chat with Your PDF Data 📄🤖")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

uploaded_file = st.file_uploader("Choose a PDF file.", type="pdf")

if "pdf_text" not in st.session_state:        # session state is a dictionary like object which stores the variables across interactions
    st.session_state.pdf_text = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if st.button("Process Pdf"):
    if not api_key:
        st.error("Error: API key is missing!")
    elif not uploaded_file:
        st.error("Error: No PDF file uploaded!")
    else:
        with st.spinner("Processing PDF..."):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)    # here processing the pdf here similar to the previous task 
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()

            if pdf_text.strip():
                st.success("PDF processed successfully! Ask questions below.")
                st.session_state.pdf_text = pdf_text                           # so here we store the texts present in the pdf folder
                st.session_state.api_key = api_key
                st.text_area("Extracted PDF Content", value=pdf_text, height=300)

            else:
                st.warning("Unable to read the uploaded PDF.")

if st.session_state.pdf_text:                                #checks if pdf is processed and stored in session state
    user_question = st.text_input("Ask a question about the PDF content:")
    if user_question:
        with st.spinner("Generating Response..."):
            prompt_template = PromptTemplate(
                input_variables=["pdf_content", "user_question"],            #here using the prompt template of langchain 
                template=(
                    "You are a helpful assistant. "
                    "Answer questions based on the provided text.\n\n"
                    "PDF Content: {pdf_content}\n\nQuestion: {user_question}"
                ),
            )

            llm = OpenAI(openai_api_key=st.session_state.api_key, temperature=0.7)
            chain = LLMChain(llm=llm, prompt=prompt_template)

            answer = chain.run(pdf_content=st.session_state.pdf_text, user_question=user_question)

            st.text_area("Response:", value=answer, height=200)


# NEW Feature learned:

#The use of st.session_state ensures that the extracted PDF content and API key persist across reruns of the app 
# (e.g., when the user submits a question). 
# This is necessary because Streamlit reruns the script every time a user interacts with the app