import json

with open("app/data/prompt.json", "r") as f:
    prompt_data = json.load(f)

def register_slack_slash_commands(slack_app):
    slack_app.command("/gpt-as-novelist")(handle_command_gpt_as_novelist)
    slack_app.command("/gpt-as-terminal")(handle_command_gpt_as_terminal)
    slack_app.command("/gpt-as-en-translator")(handle_command_gpt_as_en_translator)
    slack_app.command("/gpt-as-en-dict")(handle_command_gpt_as_en_dict)
    slack_app.command("/gpt-as-interviewer")(handle_command_gpt_as_interviewer)
    slack_app.command("/gpt-as-js-console")(handle_command_gpt_as_js_console)
    slack_app.command("/gpt-as-travel-guide")(handle_command_gpt_as_travel_guide)
    slack_app.command("/gpt-as-story-teller")(handle_command_gpt_as_story_teller)
    slack_app.command("/gpt-as-math-teacher")(handle_command_gpt_as_math_teacher)
    slack_app.command("/gpt-as-ai-doctor")(handle_command_gpt_as_ai_doctor)
    slack_app.command("/gpt-as-financer")(handle_command_gpt_as_financer)
    slack_app.command("/gpt-as-investor")(handle_command_gpt_as_investor)
    slack_app.command("/gpt-as-encoverage-book")(handle_command_gpt_as_encoverage_book)
    slack_app.command("/gpt-as-text-gamer")(handle_command_gpt_as_text_gamer)
    slack_app.command("/gpt-as-it-architect")(handle_command_gpt_as_it_architect)
    slack_app.command("/gpt-as-fullstack-dev")(handle_command_gpt_as_fullstack_dev)
    slack_app.command("/gpt-as-regex-master")(handle_command_gpt_as_regex_master)

def get_command_name(command):
    return command["command"].replace("/", "")

def build_prompt_blocks(prompt_key):
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{prompt_data[prompt_key]['name']['cn']}"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"{prompt_data[prompt_key]['prompt']['cn']}"
                },
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "---\nPlease copy the prompt to reply to me."
                }
            ]
        },
    ]

def handle_command_gpt_as_novelist(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_terminal(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_en_translator(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_en_dict(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_interviewer(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_js_console(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_travel_guide(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_story_teller(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_math_teacher(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_ai_doctor(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_financer(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_investor(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_encoverage_book(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_text_gamer(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_it_architect(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_fullstack_dev(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )

def handle_command_gpt_as_regex_master(ack, say, command):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    blocks = build_prompt_blocks(get_command_name(command))

    say(channel=channel_id,
        text=f"<@{user_id}>, let's talk!",
        blocks=blocks,
        reply_broadcast=True
    )