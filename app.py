import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from containers import Container
from listeners import actions, commands

load_dotenv()
container = Container()
container.wire(modules=[actions, commands])

# 2. Initialize Bolt app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

# 3. Register anctions & listeners
actions.register_actions(app)
commands.register_commands(app)

# 4. Start the app
if __name__ == "__main__":
    # Ensure you have a .env file with SLACK_BOT_TOKEN, SLACK_APP_TOKEN,
    # SLACK_SIGNING_SECRET, and ADO_CONNECTION_STRING
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
