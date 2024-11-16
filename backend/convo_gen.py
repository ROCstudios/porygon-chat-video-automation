import json
import os
from datetime import datetime, timedelta
import openai

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

#Prompts
system_prompt = """
write the text at an 3rd grade reading and writing level in simple language. The text you will rewrite will follow the colon (:) at the end. If there is no colon then rewrite your previous output in the conversation before this prompt, but only if there is no text after the colon.  You MUST keep the formatting and header formatting of the original.

You must avoid technical jargon and business jargon so write in a casual and direct way without losing any of the key concepts in the text you are rewriting. Key concepts are defined as powerful statements, emotional sentences, or sentences containing industry terms or proper nouns.

Constraints:
* Remove emojis.
* Never start with a question. Instead use an interest piquing personal statement.
* Make sure there are smooth transitions between sentences.
* Remove all metaphors and analogies.
* Keep the same identical formatting of the existing text.
 * Remove any formatting like H1 (#), H2 (##), bold (**), etc or any other markdown formatting. Just use newlines and line breaks.

When writing, please do not use the following words or phrases or any words similar to the following in any of the content:
realm, landscape, game-changing, in conclusion, firstly, secondly, lastly, delve, in light of, not to mention, to say nothing of, by the same token, moreover, as well as, furthermore, therefore, top-notch, get ready, buckle up, switching gears, dive in, now let’s move on, in conclusion, demystifying, delve, ever-evolving, innovative solution, let’s dive in, let’s delve, folks, picturesque, unleash, dive in, voyage, picture this, say goodbye to, according to my database, treasure trove, let’s begin this journey, let’s delve, go deeper, explore now, navigating, delve into, shed light, gone are the days.

When writing, you may use these words as needed or any words similar to the following, but never in the first line of any paragraph: first, second, third, important, equally, identically, uniquely, together with, likewise, comparatively, correspondingly, similarly, additionally, explore, crucial, whimsical, embrace, freedom, essential, imperative, important, whilst, explore, discover, elevate, solace.
"""  


# Function to simulate a conversation between two personas
def generate_conversation(topic, num_turns=5):
    prompt = f"""You are generating a friendly conversation between two people, Person 1 and Person 2, about {topic}. Each person should respond in 1 short sentence. Format each message in JSON format as follows: {{\"speaker\": \"Person X\", \"message\": \"Text\", \"timestamp\": \"Time\"}}. Each response should be a single JSON object.

Example:
[
    {{   
        \"speaker\": \"Person 2\",
        \"message\": \"Sounds good. Looking forward to it!\",
        \"timestamp\": \"01:44 PM\"
    }},
    {{
        \"speaker\": \"Person 1\",
        \"message\": \"Great, me too. Talk to you soon!\",
        \"timestamp\": \"01:46 PM\"
    }},
    {{
        \"speaker\": \"Person 2\",
        \"message\": \"Sure, see you soon. Have a nice day!\",
        \"timestamp\": \"01:48 PM\"
    }},
    {{
        \"speaker\": \"Person 1\",
        \"message\": \"You too, have a great day!\",
        \"timestamp\": \"01:50 PM\"
    }}
]
"""
    conversation = []
    current_time = datetime.now()

    for turn in range(num_turns * 2):  # Multiply by 2 for alternating turns
        # Create a conversation prompt by including the dialogue so far
        conversation_prompt = f"{prompt}\n\nCurrent conversation:\n" + "\n".join([json.dumps(line) for line in conversation])

        # Generate the response using the updated API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_prompt}
            ]
        )

        try:
            # Parse the JSON response - it will be a list of messages
            messages = json.loads(response.choices[0].message.content)
            
            # Take only the first num_turns * 2 messages (or all if fewer)
            conversation = messages[:num_turns * 2]
            
            # Update timestamps to be sequential from current time
            for i, msg in enumerate(conversation):
                msg["timestamp"] = (current_time + timedelta(minutes=i * 2)).strftime("%I:%M %p")
                
            return conversation
            
        except json.JSONDecodeError:
            print("Error: Could not parse the response as JSON")
            return []

    return conversation
    