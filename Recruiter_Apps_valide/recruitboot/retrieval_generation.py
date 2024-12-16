from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory




def create_conversation_chain(vectorstore):
    if not isinstance(vectorstore, FAISS):
        raise TypeError("Le vectorstore doit être un objet de type FAISS.")

    # Initialisation du LLM avec HuggingFaceHub
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        huggingfacehub_api_token="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",
        model_kwargs={"temperature": 0.5, "max_length": 512}
    )

    # Configuration de la mémoire pour conserver l'historique des conversations
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )

    # Création de la chaîne conversationnelle
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


