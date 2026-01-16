import json


def register_commands(app):
    @app.command("/release")
    def handle_release(ack, body, say):
        ack()
        text = body.get("text", "")
        user_id = body.get("user_id")

        args = [arg.strip() for arg in text.split(",")]

        if len(args) != 3:
            say(
                "Oops! I need 3 arguments, separated by commas.\n"
                "Correct format: `/release <source_branch>, <commit_sha_or_tag>, <target_branch>`"
            )
            return

        source_branch, source_ref, target_branch = args

        # A simple heuristic to guess if the reference is a commit or a tag
        ref_type = (
            "commit" if len(source_ref) in (7, 40) and source_ref.isalnum() else "tag"
        )

        confirmation_text = (
            f"🚀 *New Release Initiated by <@{user_id}>!* 🚀\n\n"
            f"You're about to start a new release process. Please double-check the details below:\n\n"
            f"• *Source Branch:* `{source_branch}`\n"
            f"• *From {ref_type.capitalize()}:* `{source_ref}`\n"
            f"• *Target Branch:* `{target_branch}`\n\n"
            f"Are you sure you want to proceed?"
        )

        # We serialize the arguments to pass them to the action handler
        action_value = json.dumps(
            {
                "source_branch": source_branch,
                "source_ref": source_ref,
                "target_branch": target_branch,
                "ref_type": ref_type,
            }
        )

        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": confirmation_text},
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Proceed ✅"},
                            "style": "primary",
                            "action_id": "release_proceed",  # This will be handled in actions.py
                            "value": action_value,
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Cancel 🛑"},
                            "style": "danger",
                            "action_id": "release_cancel",  # This will be handled in actions.py
                        },
                    ],
                },
            ]
        )

    @app.command("/ping")
    def handle_ping(ack, body, say):
        ack()
        user_id = body.get("user_id")
        say(f"Pong <@{user_id}>! ✅")
