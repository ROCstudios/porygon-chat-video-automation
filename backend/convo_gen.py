import json
import os
from datetime import datetime, timedelta
import openai

from config import configer
# Set up your OpenAI API key
openai.api_key = configer['OPENAI_API_KEY']

#Prompts
system_prompt = """
Write the text at an 3rd grade reading and writing level in simple language. You MUST keep the output in JSON format, specifically the JSON object properties are speaker, message, and timestamp inside json objects inside a single array.

Constraints:
* Never use emojis.
* Remove any labels, instructions, labels, or any other text that is not part of the conversation.
* ONLY OUTPUT JSON.
* Keep the same identical formatting of the existing text.
 * Remove any formatting like H1 (#), H2 (##), bold (**), etc or any other markdown formatting. Just use newlines and line breaks.

When writing, please do not use the following words or phrases or any words similar to the following in any of the content:
realm, landscape, game-changing, in conclusion, firstly, secondly, lastly, delve, in light of, not to mention, to say nothing of, by the same token, moreover, as well as, furthermore, therefore, top-notch, get ready, buckle up, switching gears, dive in, now let’s move on, in conclusion, demystifying, delve, ever-evolving, innovative solution, let’s dive in, let’s delve, folks, picturesque, unleash, dive in, voyage, picture this, say goodbye to, according to my database, treasure trove, let’s begin this journey, let’s delve, go deeper, explore now, navigating, delve into, shed light, gone are the days.

When writing, you may use these words as needed or any words similar to the following, but never in the first line of any chat: first, second, third, important, equally, identically, uniquely, together with, likewise, comparatively, correspondingly, similarly, additionally, explore, crucial, whimsical, embrace, freedom, essential, imperative, important, whilst, explore, discover, elevate, solace.
"""  


# Function to simulate a conversation between two personas
def generate_conversation(topic, num_turns=5):
    print(f"💬 GENERATE CONVERSATION: Generating conversation about {topic} with {num_turns} turns")
    prompt = f"""You are generating a friendly conversation between two people, Person 1 and Person 2, about {topic} that should only have {num_turns} text messages. Each person should respond in 1 short sentence. Format each message in JSON format as follows: {{\"speaker\": \"Person X\", \"message\": \"Text\", \"timestamp\": \"Time\"}}. Each response should be a single JSON object.


    Requirements: 
    1. Something else that is importatant is the timestamps.  They should be sequential and start with the current time like in the example below. There should be no discernable patterns to the timestamps.  For example, if the current time is 1:44 PM, the timestamps COULD BE 01:44 PM, 02:13 PM, 02:17 PM, 3:00 PM, 4:44 PM, 4:59 PM, etc.
    2. The conversations should have two people talking meaning one person can send multiple messages in a row before the other replies.  Though not all of the time, do this randomly to make it more realistic.
    3. The timestamps should be sequential and start with the current time, with no discernible patterns. Additionally, incorporate random intervals for one person to send multiple messages before the other replies to simulate a more realistic conversation flow.

Pay special attention to the timestamps and the conversation flow.  IMPORTANT TO NOTE:how one person will send multiple messages in a row before the other replies.

Now generate the conversation about {topic} with {num_turns} turns in a JSON format like the example above after the colon:

[
"""
    conversation = []
    current_time = datetime.now()

    for turn in range(int(num_turns) * 2):  # Multiply by 2 for alternating turns
        # Create a conversation prompt by including the dialogue so far
        conversation_prompt = f"{prompt}\n\nCurrent conversation:\n" + "\n".join([json.dumps(line) for line in conversation])

        # Generate the response using the updated API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_prompt}
            ],
            temperature=1.2,
            top_p=1.0
        )
        print(f"GENERATE CONVERSATION: Response: {response}")
        try:
            # Parse the JSON response - it will be a list of messages
            response_text = response.choices[0].message.content
            new_messages = json.loads(response_text)
            conversation.extend(new_messages)
            return conversation
            
        except json.JSONDecodeError:
            print("💬 GENERATE CONVERSATION: Error: Could not parse the response as JSON")
            return []

    return conversation
    