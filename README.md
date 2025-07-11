# QABot - Simple RAG-Powered Chatbot Hosted on UnityPredict

This project demonstrates how to build and deploy a Question and Answer (Q&A) chatbot using Retrieval-Augmented Generation (RAG) and FAISS (Facebook AI Similarity Search) 
for vector storage. The chatbot leverages OpenAI's Large Language Model (LLM) to answer questions based on the content of PDF files provided in a folder called `Sources`. This project automates the process of training a vector store from your PDF files and deploying a chatbot engine to UnityPredict for easy web integration.

## 🚀 Quick Start

1. **Setup UnityPredict Account & SDK**
2. **Configure your API keys in `config.env`**
3. **Add your PDF files to the `Sources` folder**
4. **Run the deployment script: `./train_and_deploy.ps1`**
5. **Create a model in UnityPredict UI (Interface Type: "Chatbot")**

## Features

- **Retrieval-Augmented Generation (RAG)**: Combines information retrieval with generation capabilities using OpenAI's LLM.
- **FAISS for Vector Storage**: Stores the vectorized content of the PDF files for fast retrieval during the Q&A process.
- **Semantic Chunking**: Uses advanced semantic text splitting for better context understanding and more accurate responses.
- **Conversational Memory**: Maintains chat history for contextual conversations across multiple interactions.
- **Integration with OpenAI and Hugging Face**: Provides responses based on information from the PDFs.
- **One-Click Deployment**: Automated training and deployment process via PowerShell script.
- **Deployment on UnityPredict**: A custom engine is created and deployed on UnityPredict, allowing users to integrate the chatbot with their web platforms.
- **Web-Ready**: Easy embedding on any website through UnityPredict's embed code.

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
     pip install unitypredict-engines
     ```

4. **UnityPredict Configuration**:
   - Run the following command to configure the UnityPredict API key on your local machine:
     ```bash
     unitypredict --configure
     ```
   - During this step, you will need to provide your UnityPredict API key.

5. **UnityPredict Repository**:
   - Create a repository on UnityPredict and note the repository ID.
   - The repository ID will be automatically added to the `config.json` file during deployment.

6. **API Keys for HuggingFace and OpenAI**:
   - Create accounts on both [HuggingFace](https://huggingface.co/) and [OpenAI](https://openai.com/).
   - Generate API keys from each service.

## Project Structure

```
QABot/
├── config.env.example        # Configuration template (copy to config.env)
├── config.env               # Your actual configuration (not in git)
├── train_and_deploy.ps1     # Automated deployment script
├── Sources/                 # Your PDF knowledge base
├── VectorStores/           # Generated vector embeddings
├── QABotTrainer/          # Training module
│   ├── Train.py           # PDF processing & vector store creation
│   └── requirements.txt   # Training dependencies
└── QABotEngine/           # Deployment module
    ├── EntryPoint.py      # Main chatbot logic with RAG implementation
    ├── main.py           # Local testing script
    ├── config.json       # UnityPredict deployment configuration
    └── requirements.txt  # Engine dependencies
```

**Key Components:**
- **QABotTrainer**: Contains the logic for training the vector store using FAISS with PDF content.
- **QABotEngine**: Contains the logic for handling the chatbot engine's interaction with OpenAI's LLM for generating answers.
- **Sources**: The folder where all your PDF files are stored. These files are used to generate the vector store.
- **EntryPoint.py**: The main entry point for the `QABotEngine`, containing the RAG implementation and conversation management.
- **Train.py**: The main entry point for the `QABotTrainer`, handling PDF processing and vector store creation.

## Configuration

1. **Create your configuration file**:
   ```bash
   # Copy the example configuration file
   cp config.env.example config.env
   ```

2. **Edit `config.env`** with your actual API keys and repository ID:
   ```env
   # OpenAI API Configuration
   OPENAI_API_KEY=your-actual-openai-api-key
   
   # Hugging Face Hub API Configuration
   HUGGINGFACEHUB_API_TOKEN=your-actual-huggingface-token
   
   # UnityPredict Configuration
   TARGET_REPOSITORY_ID=your-actual-unitypredict-repository-id
   
   # Optional: Customize model settings
   OPENAI_MODEL=gpt-4o
   TEMPERATURE=0
   ```

3. **Add your PDF files** to the `Sources` folder:
```
Sources/
├── handbook.pdf
├── manual.pdf
└── other-documents.pdf
```

The deployment script will automatically update the `config.json` file with your repository ID. If you need to manually modify other settings in `config.json`, you can edit the file directly:

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
        "ParentRepositoryId": "TARGET_REPOSITORY_ID",
        "EngineDescription": "A simple QA chatbot engine",
        "EnginePlatform": "SL_CPU_BASE_PYTHON_3.12",
        "Storage": 2048,
        "Memory": 2048
    }
}
```

## How to Use

The project includes a PowerShell script, `train_and_deploy.ps1`, that automates the entire process of training the chatbot and deploying it to UnityPredict.

### Steps to Run the Script:

1. Open PowerShell and navigate to the root of the project directory.
   
2. Ensure all prerequisites are met, and update the API keys and repository ID in the `config.env` file.

3. Run the `train_and_deploy.ps1` script to automatically:

   - Train the model by converting PDF content into vector store files using FAISS.
   - Deploy the custom engine to your UnityPredict account.

   Use this command in PowerShell:

   ```powershell
   ./train_and_deploy.ps1
   ```

### What Happens During the Script Execution:

**What the script does:**
1. ✅ Copies configuration files to sub-projects
2. ✅ Creates Python virtual environment
3. ✅ Installs all dependencies
4. ✅ Trains vector store from PDF files
5. ✅ Deploys engine to UnityPredict
6. ✅ Cleans up virtual environment

- **Training**: The script changes into the `QABotTrainer` folder, installs the required dependencies, and runs the `Train.py` script to create the vector store files from the PDF content.
- **Deploying**: After training, the script switches to the `QABotEngine` folder, installs the required dependencies, and deploys the engine to UnityPredict by running:
  
  ```bash
  unitypredict --engine --deploy
  ```

## 🌐 Final Setup in UnityPredict

After successful deployment, complete the setup in UnityPredict:

1. **Go to UnityPredict Console**
2. **Create a new Model**
3. **Configure Model Settings:**
   - **Interface Type**: Select "Chatbot"
   - **Engine**: Choose your deployed QABot engine
   - **Input Schema**: `InputMessage` (string)
   - **Output Schema**: `OutputMessage` (string)

4. **Get Embed Code**: Copy the provided embed code to your website

## Notes

- Ensure that the API keys are valid and correctly configured.
- The `Sources` folder should contain all the PDF files that the bot will use to answer questions.
- The script automates both the training and deployment process; any errors during these steps will be printed in the PowerShell console.
- The UnityPredict chatbot engine can then be linked to a UnityPredict model (created using the UnityPredict Console) and embedded directly into your website using the tools provided on the UnityPredict platform.

## 🧪 Testing Locally

Test your chatbot before deployment:

```bash
cd QABotEngine
python main.py
```

This will run a test query: "What questions can you help me with?"

## 🔍 How It Works

1. **Training Phase**:
   - Loads PDF files from `Sources/` folder
   - Splits documents using semantic chunking
   - Creates FAISS vector embeddings
   - Saves to `VectorStores/` directory

2. **Inference Phase**:
   - Loads trained vector store
   - Uses RAG to retrieve relevant context
   - Generates responses with OpenAI
   - Maintains conversation history

3. **Deployment**:
   - Packages engine for UnityPredict
   - Deploys with specified resources
   - Makes chatbot available via API

## 🚨 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure you're using Python 3.12
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**UnityPredict deployment fails:**
- Verify API key: `unitypredict --configure`
- Check repository ID in `config.env`
- Ensure repository exists in UnityPredict

**PDF processing errors:**
- Verify PDF files are not corrupted
- Check file permissions in `Sources/` folder
- Ensure sufficient disk space for vector store

**API key errors:**
- Verify OpenAI API key has sufficient credits
- Check HuggingFace token permissions
- Ensure keys are correctly set in `config.env`

### Debug Mode
Enable detailed logging by checking the console output during deployment. The script provides step-by-step feedback.

**Original troubleshooting notes:**
- **Module Not Found**: Ensure that the correct Python version is being used and all dependencies are installed by running `pip install -r requirements.txt` in the `QABotTrainer` and `QABotEngine` folders.
- **UnityPredict Deployment Issues**: Ensure that your API key and repository name are correct and the `unitypredict --configure` command has been run on your local machine.
- **API Key Errors**: Double-check the `HUGGINGFACEHUB_API_TOKEN` and `OPENAI_API_KEY` values in `EntryPoint.py` and `Train.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
