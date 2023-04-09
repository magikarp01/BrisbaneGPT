import embed_files
import chat_files

queries = [
    "Can you summarize national housing sale trends, including price changes and ownership trends?",
    "Can you summarize housing trends in the Maryland area, including Baltimore?",
"Can you summarize the points made in Bright_Monthly_Market_Report_Washington_DC_March_2022.pdf?",
"Are houses generally becoming more or less affordable across the nation?",
]

embed_files.generate_embeddings('./embeddings/housing-dir', "./demo-files/housing", chunk_size=300)

housing_chatbot = chat_files.make_chatbot("./embeddings/housing-dir", top_k_docs=10)
for query in queries:
    print(f"Asking query: {query}")
    chat_files.ask_query(housing_chatbot, query)
    print("\n\n\n")
