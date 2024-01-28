def process_google_drive_documents(
    documents,
):
    def process_google_drive_document(document):
        document.id_ = document.metadata["file_name"]
        return document
