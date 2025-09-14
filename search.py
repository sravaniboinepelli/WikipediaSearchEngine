from query import search
from time import time as t

title_map = {}
with open("Test/mapping.txt", encoding="utf8") as f:
    for line in f:
        doc_id = line.split()[0]
        try:
            title = " ".join(line.split()[1:])
        except:
            title = "id:" + line.split()[0] + ". Filename not found"
        title_map[int(doc_id)] = title

if __name__ == "__main__":
    print("Enter query to search and type '.' to end the loop")
    while True:
        string = input("Enter your query : ")
        if string.strip() == ".":
            break
        start = t()
        doc_list = search(string)
        if not doc_list:
            print("No results found")
        for k in doc_list:
            if k in title_map:
                print(title_map[k])
        print("Time taken:", t() - start)
