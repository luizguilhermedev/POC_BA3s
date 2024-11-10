# Project Documentation

## Overview
This project is a Python-based application that leverages various AI models and tools to analyze book reviews and provide insights. It uses the LangChain library for creating chains of document processing and retrieval, and integrates with multiple APIs for language models.

## Project Structure
- `rag_implementation_app.py`: Main application file for the Retrieval-Augmented Generation (RAG) implementation.
- `agent_implementation_app.py`: Main application file for the agent-based implementation using Streamlit for the UI.
- `src/utils.py`: Utility functions for model retrieval, embedding, and session management.
- `src/constants.py`: Contains constants used across the project.
- `app.py`: Entry point for initializing the chatbot UI.


## Main Components


### `agent_implementation_app.py`
This file sets up an agent-based application using Streamlit:
- Imports necessary modules and functions.
- Initializes the agent and session factory.
- Defines functions to handle user input and extract code from responses.
- Sets up the Streamlit UI for user interaction and displays responses.

### `src/utils.py`
This file contains utility functions:
- `get_llm_model(use_openai: bool)`: Returns the language model based on the specified API.
- `get_agent(path: list[str])`: Creates and returns a CSV agent.
- `get_embedding_model()`: Returns the embedding model.
- `get_retriever()`: Returns the retriever for the vector store.
- `create_session_factory(base_dir: Union[str, Path])`: Creates a session factory for chat histories.
- `InputChat`: Pydantic model for chat input.
- `extract_code_from_response(response)`: Extracts Python code from a string response.

### `src/constants.py`
This file contains constants used across the project:
- `APP_PORT`: Port number for the application.
- `LOG_LEVEL`: Logging level for the application.

### `app.py`
This file initializes the chatbot UI:
- Imports the `initialize_chatbot_ui` function from `src/utils.py`.
- Calls the `initialize_chatbot_ui` function to start the Streamlit application.


## Installation
1. Clone the repository.
2. Set up the environment variables in the `.env` file.


To run the agent-based application:
```sh
streamlit run agent_implementation_app.py
```

## Running the Application with Docker
```sh
docker compose -f docker-compose.yaml up --build
```

## License
This project is licensed under the MIT License.