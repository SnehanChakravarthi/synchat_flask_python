# synchat_flask_python

## (Optional) Create and activate a virtual environment for development

It's a good practice to use a virtual environment for this project. This keeps dependencies for this project separate and organized. To create and activate a virtual environment, run the following commands in your terminal:

```bash
python -m venv .myenv
source .myenv/bin/activate  # On Unix or MacOS
myenv\Scripts\activate  # On Windows
```

## Install Dependencies

To install the necessary dependencies for this project, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

# Environment Setup Instructions

To configure your local environment for this project, follow these steps:

## Step 1: Create `.env` File

Create a file named `.env` in the root directory of the project. This file will store important environment variables.

## Step 2: Add Environment Variables

Open the `.env` file and add the following environment variables:

```plaintext
PORT=3000
ACCESS_TOKEN=
PHONE_NUMBER_ID=
VERIFICATION_TOKEN=
APP_SECRET=
OPENAI_API_KEY=
```

## Start the server

```bash
python run.py
```

This project was created using `flask`.
