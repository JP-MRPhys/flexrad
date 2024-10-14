from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain, RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings


class LLM:
    def __init__(self, model_name='llama3.1') -> None:


        self.llm=Ollama(model=model_name)

        self.template = """You are an intelligent chatbot to help summary of the medical report
        text: {text}
        Answer:"""

        self.prompt_summary = PromptTemplate(template=self.template, input_variables=["text"])
        self.summarize_chain =  self.prompt_summary | self.llm

        self.template2 = """You are an intelligent chatbot, please detect key organs, techical words and medical words and provide a summary of those words only don't interpret the report and once you have keywords please explain each keywords, provide output in json format
        text: {text}
        Answer:"""
        self.prompt_keyword = PromptTemplate(template=self.template2, input_variables=["text"])
        self.keyword_chain =  self.prompt_keyword | self.llm
        
        self.chatbot=self.create_vector_QA()

         
    def create_vector_QA(self, vector_store=None):

        if vector_store is not None:
            qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="chatbot", retriever=vector_store)
        else:
            qa_chain =RetrievalQA.from_chain_type(llm=self.llm, chain_type="chatbot", retriever=None)
        
        return qa_chain

    def get_QA(self, question):
        return self.chatbot.invoke(question)

    def get_summary(self, text):
        return self.summarize_chain.invoke(text)
    
    def get_keywords(self, text):
        return self.keyword_chain.invoke(text)
    
    def chat(self,question):
        return self.chatbot(question)
    

class data:
        def __init__(self, file_path) -> None:

            
            self.hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            self.file_path=file_path

        def create_vector_store(self):

            pages=self.get_pdf(self.file_path)   
            chunks=self.get_chunks(pages)
            vector_store = FAISS.from_documents(chunks, self.hf_embeddings)
  
            return vector_store.as_retriever()


        def get_pdf(self, file_path):
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()

            count=0
            for page in pages:
                count+=1

            print(count)

            print(pages[3])

            # Ensure all pages are strings, filter out any None or non-text pages
            large_text = " ".join([str(page) for page in pages if page is not None])

            

            if not large_text:
                raise ValueError("No valid text extracted from the PDF.")


            return large_text


           
        def get_chunks(self,large_text):


            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_text(large_text)
            documents = [Document(page_content=doc) for doc in docs]


            return documents
        
    


if __name__ == '__main__':

    test=LLM(model_name='llama3.1')
    

    """
    response=test.test_chain('how are you')
    print(response)
    
    """
    

    file='~/Downloads/test.PDF'
    daily_data=data(file_path=file)
    vector_store=daily_data.create_vector_store()

    qa_chain = RetrievalQA.from_chain_type(llm=test.llm, chain_type="stuff", retriever=vector_store)
    ans=qa_chain.invoke("Ask me a valid question")
    print(ans)

    
