import json

from dependency_injector.wiring import Provide, inject

from containers import Container
from services.release_service import ReleaseService


def handle_release_proceed(ack, body, client, say):
    # Bolt injects known args and passes None for unknown ones, which overrides DI defaults.
    # Keep DI-only params out of this signature so @inject can supply the real service.
    # Not sure about this!!!!!!!!!!!!!!!
    _handle_release_proceed(ack, body, client, say)


@inject
def _handle_release_proceed(
    ack,
    body,
    client,
    say,
    release_service: ReleaseService = Provide[Container.release_service],
):
    ack()
    user_id = body["user"]["id"]

    try:
        # Update the original message to remove the buttons
        original_blocks = body["message"]["blocks"]
        original_blocks.pop(1)  # Remove the buttons
        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            blocks=original_blocks,
        )

        say(
            thread_ts=body["message"]["ts"],
            text=f"🏃‍♂️ Okay <@{user_id}>, starting the release... please wait.",
        )

        # Parse the data we stored in the button's value
        action_value = json.loads(body["actions"][0]["value"])
        source_branch = action_value["source_branch"]
        source_ref = action_value["source_ref"]
        target_branch = action_value["target_branch"]

        # Call the service to perform the action
        success = release_service.create_branch(
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


def handle_release_cancel(ack, body, client, say):
    ack()
    user_id = body["user"]["id"]

    # Post the cancellation message in a thread
    say(
        thread_ts=body["message"]["ts"],
        text=f"❌ Release cancelled by <@{user_id}>.",
    )

    # Update the original message to remove the buttons
    original_blocks = body["message"]["blocks"]
    original_blocks.pop(1)  # Remove the buttons
    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        blocks=original_blocks,
    )


def register_actions(app):
    app.action("release_proceed")(handle_release_proceed)
    app.action("release_cancel")(handle_release_cancel)
