import os
import re

class SimpleSearchEngine:
    def __init__(self, directory):
        self.directory = directory
        self.index = {}
        self.build_index()

    def build_index(self):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".txt"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                        words = re.findall(r'\w+', text.lower())
                        for word in words:
                            if word not in self.index:
                                self.index[word] = set()
                            self.index[word].add(filepath)

    def search(self, query):
        keywords = re.findall(r'\w+', query.lower())
        results = None
        for word in keywords:
            if word in self.index:
                if results is None:
                    results = self.index[word].copy()
                else:
                    results &= self.index[word]
            else:
                return []
        return sorted(results) if results else []

if __name__ == "__main__":
    engine = SimpleSearchEngine(".") # Current directory
    while True:
        query = input("Enter search query (or 'exit'): ")
        if query.lower() == "exit":
            break
        results = engine.search(query)
        if results:
            print("Found in files:")
            for file in results:
                print(" -", file)
        else:
            print("No results found.")