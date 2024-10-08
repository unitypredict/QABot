# Store the current directory
$originalDir = Get-Location

Write-Host "Creating virtual environment..." -ForegroundColor Green

python -m venv .venv

.\.venv\Scripts\Activate

Write-Host "Installing requirements for training script..." -ForegroundColor Green

# Step 1: Change to the QABotTrainer directory and install dependencies
cd "QABotTrainer"
python -m pip install --upgrade --quiet  -r requirements.txt

Write-Host "Running training script..." -ForegroundColor Green

# Step 2: Run the Train.py script to create vector store files
python Train.py

# Step 3: Change back to the original directory
cd $originalDir

Write-Host "Installing requirements for the engine..." -ForegroundColor Green

# Step 4: Change to the QABotEngine directory and install dependencies
cd "QABotEngine"
python -m pip install --upgrade --quiet -r requirements.txt

Write-Host "Deploying UnityPredict Engine..." -ForegroundColor Green

# Step 5: Run the deploy command
unitypredict --engine --deploy

cd $originalDir

# Step 5: Deactivate the virtual environment when done
Deactivate