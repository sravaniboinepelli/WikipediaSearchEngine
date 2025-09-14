## How it works

The search engine consists of two main parts: **indexing** and **searching**. This project has been successfully tested on a 46GB Wikipedia dump. The current repository, however, contains index files for a smaller 100MB dump for easier access, so all searches will be performed on this smaller dataset. The full 14GB index files were omitted due to their size.

---

### Indexing

The indexing process converts a Wikipedia XML dump into a searchable text file. The index stores words and their associated document IDs, along with how often each word appears in a specific document. Before indexing, the text undergoes several preprocessing steps:

1.  **Tokenization**: The text is broken down into individual words or "tokens."
2.  **Stop word removal**: Common words like "the," "a," and "is" are removed since they don't contribute much to relevance.
3.  **Stemming**: Words are reduced to their root form (e.g., "running" becomes "run") to improve search accuracy.

The frequency of words is also categorized by their location within a document, such as the **title**, **body**, **categories**, or **links**. For very large files, like the 46GB dump, the **Single-Pass In-Memory Indexing algorithm** is used to sort the index efficiently.

To optimize query time, the main index is partitioned into 36 smaller indexes, each dedicated to words starting with a specific letter or number (e.g., `p.txt` for words starting with "p").

To index an XML dump, run:
`python3 index.py xmlfile indexfolder`

*Note: All index files must be located within the index folder.*
---

### Searching

The search component sifts through the index to find and rank the most relevant documents, displaying the top results along with the time taken to process the query. Document relevance is determined using two key metrics:

* **TF-IDF (Term Frequency-Inverse Document Frequency) scores**: This metric measures how important a word is to a document within the entire dataset.
* **Cosine similarity**: This calculates the similarity between the search query and each document based on their TF-IDF values. The top 10 documents with the highest cosine similarity are selected.

To speed up calculations, **champions lists** are used. This pre-selection process narrows down the search to the top 20 documents with the highest TF-IDF scores, significantly reducing the number of cosine similarity computations.

After the relevant document IDs are identified, a mapping file is used to retrieve their corresponding titles, which are then displayed to the user.

To run the search engine, use:
`python3 search.py`

