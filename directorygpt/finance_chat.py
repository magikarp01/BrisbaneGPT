import embed_files
import chat_files

# embed_files.generate_embeddings('./embeddings/finance-dir', "./demo-files/finance")
query = "How is the budget deficit funded, using only evidence from the provided files?"
finance_chatbot = chat_files.make_chatbot("./embeddings/finance-dir", top_k_docs=6)
chat_files.ask_query(finance_chatbot, query)
