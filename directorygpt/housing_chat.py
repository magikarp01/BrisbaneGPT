import embed_files
import chat_files

# embed_files.generate_embeddings('./embeddings/housing-dir', "./demo-files/housing", chunk_size=300)
query = "Can you summarize national housing sale trends, including price changes and ownership trends?"
# query = "Can you summarize housing trends in the Maryland area, including Baltimore?"
# query = "Can you summarize the points made in Bright_Monthly_Market_Report_Washington_DC_March_2022.pdf?"
finance_chatbot = chat_files.make_chatbot("./embeddings/housing-dir", top_k_docs=10)
chat_files.ask_query(finance_chatbot, query)
