from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader(
    path = "./example_data/",
    glob = "**/[!.]*.pdf",
)