from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain_community.vectorstores import Chroma

import utils as u


def ingest_data(path):
    # Load the data

    loader = DirectoryLoader(path, glob='**/*.csv', loader_cls=CSVLoader)
    documents = loader.load_and_split()

    try:
        vector_db = Chroma.from_documents(
            documents,
            embedding=u.get_embedding_model(),
            persist_directory='vectordb_data/',
        )
        return 'Ingested data successfully'

    except:
        raise Exception('Error while ingesting data')


if __name__ == '__main__':

    """Execute the ingestion process"""

    ingest_data('data/')
