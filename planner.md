## 📝 Notes

- Mixtral is heavy (~40GB). Use `mistral` or `llama2` for lighter local testing.
- Chroma stores everything locally (no server needed).
- DuckDB (used by Chroma) is embedded and doesn’t need setup.
- Ensure `persist_directory` is consistent to avoid re-embedding.
- nomic-embed-text only embeds texts and pdfs. Cannot embed images.
- apply hashing to documents to prevent duplication in vector db with the same files.
- Create makefile to start streamlit
- Write a better prompt so that it doesnt only reply based on documents

---


