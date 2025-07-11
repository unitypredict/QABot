# Store the current directory
$originalDir = Get-Location

# Check if config.env exists
if (-not (Test-Path "config.env")) {
    Write-Host "ERROR: config.env file is missing!" -ForegroundColor Red
    Write-Host "" -ForegroundColor Red
    Write-Host "To fix this:" -ForegroundColor Yellow
    Write-Host "1. Copy the example configuration file:" -ForegroundColor Yellow
    Write-Host "   cp config.env.example config.env" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor Yellow
    Write-Host "2. Edit config.env with your actual API keys and repository ID" -ForegroundColor Yellow
    Write-Host "3. Run this script again" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Red
    exit 1
}

Write-Host "Configuration file found. Proceeding with deployment..." -ForegroundColor Green
Write-Host "Copying configuration files to sub-projects..." -ForegroundColor Green

# Copy the root config.env to both sub-projects as env.config
Copy-Item "config.env" -Destination "QABotTrainer\env.config" -Force
Copy-Item "config.env" -Destination "QABotEngine\env.config" -Force

# Get the repository ID from config.env and update config.json
$configContent = Get-Content "config.env" | Where-Object { $_ -match "^TARGET_REPOSITORY_ID=" }
if ($configContent) {
    $repositoryId = $configContent -replace "^TARGET_REPOSITORY_ID=", ""
    $repositoryId = $repositoryId.Trim()
    if ($repositoryId -and $repositoryId -ne "your-unitypredict-repository-id-here") {
        $configJsonContent = Get-Content "QABotEngine\config.json" -Raw
        $configJsonContent = $configJsonContent -replace '"TARGET_REPOSITORY_ID"', "`"$repositoryId`""
        Set-Content "QABotEngine\config.json" -Value $configJsonContent -NoNewline
        Write-Host "Updated config.json with repository ID: $repositoryId" -ForegroundColor Green
    } else {
        Write-Host "Warning: TARGET_REPOSITORY_ID not set or using placeholder value" -ForegroundColor Yellow
    }
} else {
    Write-Host "Warning: TARGET_REPOSITORY_ID not found in config.env" -ForegroundColor Yellow
}

Write-Host "Creating virtual environment..." -ForegroundColor Green

python -m venv .venv

.\.venv\Scripts\Activate

Write-Host "Installing unitypredict-engines Package..." -ForegroundColor Green

python -m pip install --upgrade --quiet unitypredict-engines

Write-Host "Installing requirements for training script..." -ForegroundColor Green

# Step 1: Change to the QABotTrainer directory and install dependencies
cd "QABotTrainer"
python -m pip install --upgrade -r requirements.txt

Write-Host "Running training script..." -ForegroundColor Green

# Step 2: Run the Train.py script to create vector store files
python Train.py

# Step 3: Change back to the original directory
cd $originalDir

Write-Host "Installing requirements for the engine..." -ForegroundColor Green

# Step 4: Change to the QABotEngine directory and install dependencies
cd "QABotEngine"
python -m pip install --upgrade -r requirements.txt

Write-Host "Deploying UnityPredict Engine..." -ForegroundColor Green

# Step 5: Run the deploy command
# Note: Make sure UnityPredict is configured first with 'unitypredict --configure'
unitypredict --engine --deploy

cd $originalDir

# Step 5: Deactivate the virtual environment when done
Deactivate