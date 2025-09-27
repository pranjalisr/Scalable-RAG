from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

openai_client = OpenAI()

# Vector embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="cover_letter",
    embedding=embedding_model,
)


def process_query(query: str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([
        f"Page Content: {doc.page_content}\n"
        f"Page Number: {doc.metadata.get('page_label')}\n"
        f"File Location: {doc.metadata.get('source')}"
        for doc in search_results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers user query based on available 
    context retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )

    return response.choices[0].message.content
