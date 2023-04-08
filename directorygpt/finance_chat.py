import embed_files
import chat_files

# embed_files.generate_embeddings('./embeddings/finance-dir', "./demo-files/finance")
# query = "How is the budget deficit funded, using only evidence from the provided files?"
query = "How do interest rates set by the Federal Reserve affect US federal policy? "
finance_chatbot = chat_files.make_chatbot("./embeddings/finance-dir", top_k_docs=5)
chat_files.ask_query(finance_chatbot, query)
