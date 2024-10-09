# Question and Answer Bot using RAG and FAISS with OpenAI Integration

This project demonstrates how to build and deploy a Question and Answer (Q&A) chatbot using Retrieval-Augmented Generation (RAG) and FAISS (Facebook AI Similarity Search) for vector storage. The chatbot leverages OpenAI's Large Language Model (LLM) to answer questions based on the content of PDF files provided in a folder called `Sources`.

The project is designed to be deployed on the UnityPredict platform, allowing users to embed a chatbot interface on their websites.

## Features

- **Retrieval-Augmented Generation (RAG)**: Combines information retrieval with generation capabilities using OpenAI's LLM.
- **FAISS for Vector Storage**: Stores the vectorized content of the PDF files for fast retrieval during the Q&A process.
- **Integration with OpenAI and Hugging Face**: Provides responses based on information from the PDFs.
- **Deployment on UnityPredict**: A custom engine is created and deployed on UnityPredict, allowing users to integrate the chatbot with their web platforms.

## Prerequisites

Before running the project, ensure you have the following:

1. **UnityPredict Account**:
   - Create a free UnityPredict account by signing up at [UnityPredict](https://unitypredict.com).
   - Create an API key for authentication with UnityPredict.

2. **Python 3.12**:
   - Download and install Python 3.12 from the [official Python website](https://www.python.org/downloads/).

3. **UnityPredict Engines**:
   - Install the UnityPredict Engines SDK by running the following command:
     ```bash
     pip install unitypredict_engines
     ```

4. **UnityPredict Configuration**:
   - Run the following command to configure the UnityPredict API key on your local machine:
     ```bash
     unitypredict --configure
     ```
   - During this step, you will need to provide your UnityPredict API key.

5. **UnityPredict Repository**:
   - Create a repository on UnityPredict and add the repository information to the `config.json` file located in the root of this project.

6. **API Keys for HuggingFace and OpenAI**:
   - Create accounts on both [HuggingFace](https://huggingface.co/) and [OpenAI](https://openai.com/).
   - Generate API keys from each service.
   - Add the following environment variables in the `EntryPoint.py` file located under the `QABotEngine` folder and `Train.py` file located under the `QABotTrainer` folder:
     - `HUGGINGFACEHUB_API_TOKEN`
     - `OPENAI_API_KEY`

## Project Structure

- **QABotTrainer**: Contains the logic for training the vector store using FAISS with PDF content.
- **QABotEngine**: Contains the logic for handling the chatbot engine's interaction with OpenAI's LLM for generating answers.
- **Sources**: The folder where all your PDF files are stored. These files are used to generate the vector store.
- **EntryPoint.py**: The main entry point for both the `QABotEngine`, containing your API keys for HuggingFace and OpenAI.
- **Train.py**: The main entry point for the `QABotTrainer`, containing your API keys for HuggingFace and OpenAI.

## Configuration

### Step 1: UnityPredict Configuration

After creating your UnityPredict account and API key, run the following to configure the UnityPredict CLI. You will be asked to enter your API key to allow access to your UnityPredict account:

```bash
unitypredict --configure
```

This will ensure that the API key is stored locally for authentication during deployment.

### Step 2: Modify config.json

Ensure the config.json file has the correct repository information for UnityPredict. This file should look something like this:

```json
{
    "ModelsDirPath": "..\\VectorStores",
    "LocalMockEngineConfig": {
        "TempDirPath": "./unitypredict_mocktool/tmp",
        "RequestFilesDirPath": "./unitypredict_mocktool/requests",
        "SAVE_CONTEXT": true,
        "UPT_API_KEY": ""
    },
    "DeploymentParameters": {
        "UnityPredictEngineId": "",
        "ParentRepositoryId": "your-unitypredict-repository-id",
        "EngineDescription": "A simple QA chatbot engine",
        "EnginePlatform": "SL_CPU_BASE_PYTHON_3.12",
        "Storage": 2048,
        "Memory": 2048
    }
}
```


### Step 3: Update EntryPoint.py

In both the QABotTrainer and QABotEngine folders, modify the EntryPoint.py file to include your API keys for Hugging Face and OpenAI:

```python
# Set your HuggingFace and OpenAI API keys here
os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'your-huggingface-api-key'
os.environ["OPENAI_API_KEY"] = 'your-openai-api-key'
```

## How to Use

The project includes a PowerShell script, `train_and_deploy.ps1`, that automates the entire process of training the chatbot and deploying it to UnityPredict.

### Steps to Run the Script:

1. Open PowerShell and navigate to the root of the project directory.
   
2. Ensure all prerequisites are met, and the correct API keys are configured.

3. Run the `train_and_deploy.ps1` script to automatically:

   - Train the model by converting PDF content into vector store files using FAISS.
   - Deploy the custom engine to your UnityPredict account.

   Use this command in PowerShell:

   ```powershell
   ./train_and_deploy.ps1
   ```

### What Happens During the Script Execution:

- **Training**: The script changes into the `QABotTrainer` folder, installs the required dependencies, and runs the `Train.py` script to create the vector store files from the PDF content.
- **Deploying**: After training, the script switches to the `QABotEngine` folder, installs the required dependencies, and deploys the engine to UnityPredict by running:
  
  ```bash
  unitypredict --engine --deploy
  ```

## Notes

- Ensure that the API keys are valid and correctly configured.
- The `Sources` folder should contain all the PDF files that the bot will use to answer questions.
- The script automates both the training and deployment process; any errors during these steps will be printed in the PowerShell console.
- The UnityPredict chatbot engine can then be linked to a UnityPredict model (created using the UnityPredict Console) and embedded directly into your website using the tools provided on the UnityPredict platform.

## Troubleshooting

- **Module Not Found**: Ensure that the correct Python version is being used and all dependencies are installed by running `pip install -r requirements.txt` in the `QABotTrainer` and `QABotEngine` folders.
- **UnityPredict Deployment Issues**: Ensure that your API key and repository name are correct and the `unitypredict --configure` command has been run on your local machine.
- **API Key Errors**: Double-check the `HUGGINGFACEHUB_API_TOKEN` and `OPENAI_API_KEY` values in `EntryPoint.py` and `Train.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
