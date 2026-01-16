import json

from dependency_injector.wiring import Provide, inject

from containers import Container
from services.dev_ops_service import DevOpsService


def register_actions(app):
    @app.action("release_proceed")
    @inject
    def handle_release_proceed(
        ack,
        body,
        client,
        say,
        dev_ops_service: DevOpsService = Provide[Container.dev_ops_service],
    ):
        ack()
        user = body["user"]["name"]

        try:
            # Update the original message to show it's in progress
            original_blocks = body["message"]["blocks"]
            original_blocks[0]["text"]["text"] = (
                f"🏃‍♂️ Okay @{user}, starting the release... please wait."
            )
            original_blocks.pop(1)  # Remove the buttons
            client.chat_update(
                channel=body["channel"]["id"],
                ts=body["message"]["ts"],
                blocks=original_blocks,
            )

            # Parse the data we stored in the button's value
            action_value = json.loads(body["actions"][0]["value"])
            source_branch = action_value["source_branch"]
            source_ref = action_value["source_ref"]
            target_branch = action_value["target_branch"]

            # Call the service to perform the action
            success = dev_ops_service.create_branch(
                source_branch, source_ref, target_branch
            )

            if success:
                say(
                    thread_ts=body["message"]["ts"],
                    text=f"✅ Success! Branch `{target_branch}` was created.",
                )
            else:
                say(
                    thread_ts=body["message"]["ts"],
                    text=f"🚨 Error! Failed to create branch `{target_branch}`.",
                )

        except Exception as e:
            say(
                thread_ts=body["message"]["ts"],
                text=f"An unexpected error occurred: {e}",
            )

    @app.action("release_cancel")
    def handle_release_cancel(ack, body, client):
        ack()
        user = body["user"]["name"]

        # Update the original message to show it was cancelled
        original_blocks = body["message"]["blocks"]
        original_blocks[0]["text"]["text"] = f"❌ Release cancelled by @{user}."
        original_blocks.pop(1)  # Remove the buttons
        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            blocks=original_blocks,
        )
