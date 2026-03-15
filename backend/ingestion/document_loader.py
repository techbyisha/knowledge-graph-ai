import os

class DocumentLoader:
    def __init__(self, folder_path: str):
        """
        Initialize the document loader with the folder path
        """
        self.folder_path = folder_path

    def load_documents(self):
        """
        Load all .txt files from the folder
        Returns a list of documents
        """
        documents = []

        if not os.path.exists(self.folder_path):
            raise Exception(f"Folder not found: {self.folder_path}")

        for filename in os.listdir(self.folder_path):

            if filename.endswith(".txt"):

                file_path = os.path.join(self.folder_path, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as file:

                        content = file.read()

                        documents.append({
                            "filename": filename,
                            "content": content
                        })

                except Exception as e:
                    print(f"Error reading file {filename}: {e}")

        return documents