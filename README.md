# 🚢 Shipit Bot

A simple proof-of-concept Slack bot built with Python and `slack-bolt` to manage a basic release process via Slack commands.

## ✨ Features

-   **/release Command**: Initiate a new release process with a slash command.
-   **Interactive Confirmation**: Presents an interactive confirmation message in Slack using Block Kit.
-   **Dependency Injection**: Uses `dependency-injector` for clean, decoupled architecture.
-   **Containerized**: Comes with a multi-stage `Dockerfile` for building an optimized and secure container image.
-   **Modern Tooling**: Uses `uv` for fast dependency and environment management.

## 🛠️ Tech Stack

-   **Language**: Python 3.13+
-   **Framework**: `slack-bolt`
-   **Dependency Management**: `uv`
-   **Dependency Injection**: `dependency-injector`
-   **Containerization**: Docker

## 🚀 Getting Started

Follow these instructions to get the bot running on your local machine for development and testing.

### Prerequisites

-   Python 3.13 or higher
-   [uv](https://github.com/astral-sh/uv) (Python package installer)
-   [Docker](https://www.docker.com/get-started)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd shipit-bot
    ```

2.  **Create a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    This project uses `pyproject.toml` to define dependencies.
    ```bash
    # To install from the lock file (recommended)
    uv sync

    # Or, to install directly from pyproject.toml
    # uv pip install .
    ```

### Configuration

The application requires several secret tokens and configuration values to run. These are managed using a `.env` file.

1.  **Create a `.env` file:**
    Copy the provided example or create a new file named `.env` in the project root.

2.  **Add the following variables:**
    You will need to get these values from your Slack App configuration dashboard and your Azure DevOps account.

    ```dotenv
    # Your bot's OAuth token (starts with xoxb-)
    SLACK_BOT_TOKEN=xoxb-your-token

    # The token for Socket Mode (starts with xapp-)
    SLACK_APP_TOKEN=xapp-your-socket-token

    # Found in your Slack App's "Basic Information" page under "App Credentials"
    SLACK_SIGNING_SECRET=your-signing-secret
    ```

## ⚙️ Usage

### Running Locally

1.  Ensure your virtual environment is activated and your `.env` file is configured.
2.  Start the bot:
    ```bash
    python app.py
    ```

### Running with Docker

The project is configured to be built and run as a Docker container.

1.  **Build the Docker image:**
    ```bash
    docker build -t shipit-bot .
    ```

2.  **Run the container:**
    This command securely passes your `.env` file to the container at runtime.
    ```bash
    docker run -d --name shipit-bot --env-file .env shipit-bot:latest
    ```

### Bot Commands

-   **/release**: Initiates the release workflow.
    -   **Format**: `/release <source_branch>, <commit_sha_or_tag>, <target_branch>`
    -   **Example**: `/release develop, a3f5c9e, release/2.211.0`
-   **/ping**: A simple health-check command. The bot will reply with "Pong!".

### Screenshot of the Shipit Bot in action
<img width="624" height="509" alt="image" src="https://github.com/user-attachments/assets/9b7e3028-5584-49c3-829c-d33131c1c6d0" />


## 📂 Project Structure

```
.
├── listeners/        # Slack event listeners (actions, commands)
│   ├── actions.py
│   └── commands.py
├── services/           # Business logic (e.g., interacting with DevOps APIs)
│   └── dev_ops_service.py
├── .env                # Secret tokens and configuration (not committed)
├── app.py              # Main application entry point
├── containers.py       # Dependency injection container setup
├── Dockerfile          # For building the production container image
├── pyproject.toml      # Project definition and dependencies
└── README.md           # This file
```

