import json
import os
from datetime import datetime, timedelta
import openai

from config import configer
# Set up your OpenAI API key
openai.api_key = configer['OPENAI_API_KEY']
model = "gpt-4o-mini"
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
"""  


# Function to simulate a conversation between two personas
def generate_conversation(topic, num_turns=5):
    print(f"💬 GENERATE CONVERSATION: Generating conversation about {topic} with {num_turns} turns")
    prompt = f"""You are generating a friendly conversation between two people, Person 1 and Person 2, about {topic} that should only have {num_turns} text messages. Each person should respond in 1 short sentence. Format each message in JSON format as follows: {{\"speaker\": \"Person X\", \"message\": \"Text\", \"timestamp\": \"Time\"}}. Each response should be a single JSON object.

    Generate time stamps for a series of conversations with a pattern that appears random, with frequent but random timestamps, and random gaps in time between them, all less than 5 minutes. The timestamps should create the impression of frequent communication between the parties involved while also introducing random pauses to simulate realistic conversation flow. The pattern should not be discernable and should appear genuinely spontaneous and natural, contributing to the authenticity of the overall interaction.

    Requirements: 
    1. The conversations should have two people talking meaning one person can send multiple messages in a row before the other replies.  Though not all of the time, do this randomly to make it more realistic.
    2. Additionally, incorporate random intervals for one person to send multiple messages before the other replies to simulate a more realistic conversation flow.

IMPORTANT TO NOTE:how one person will send multiple messages in a row before the other replies.
The timestamps must be in format I%:M% %p for examples 12:11 AM.
There should be no discernable pattern to the timestamps.  The timestamps should appear random.  This is very important to me, peraonally.

Here is an example of the conversation format you MUST ALWAYS FOLLOW:
[
    {{"speaker": "Person 1", "message": "Hello, how are you?", "timestamp": "12:00 AM"}},
    {{"speaker": "Person 1", "message": "I'm doing great, thanks for asking!", "timestamp": "12:01 AM"}},
    {{"speaker": "Person 1", "message": "What's new in your life?", "timestamp": "12:01 AM"}},
    {{"speaker": "Person 2", "message": "Not much, just the usual stuff.", "timestamp": "12:03 AM"}},
    {{"speaker": "Person 2", "message": "What are you up to?", "timestamp": "12:08 AM"}},
    {{"speaker": "Person 1", "message": "Just hanging out and relaxing.", "timestamp": "12:09 AM"}},
]

Now generate the conversation about {topic} with {num_turns} turns in a JSON format.  You MUST have at least 1 instance where 2 messages in a row where one person sends multiple messages in a row before the other replies.  

[
"""
    conversation = []
    current_time = datetime.now()

    for turn in range(int(num_turns) * 2):  # Multiply by 2 for alternating turns
        # Create a conversation prompt by including the dialogue so far
        conversation_prompt = f"{prompt}\n\nCurrent conversation:\n" + "\n".join([json.dumps(line) for line in conversation])

        # Generate the response using the updated API
        response = openai.chat.completions.create(
            model=model,
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
    
def generate_image(prompt):
    try:
        # gpt prompt generation from prompt parameter
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": """
You are a prompt generator for an image generation AI. You will be given a prompt and you will need to generate a new prompt for the image generation AI.

Your job is to take the original which is a conversation between two people and extract the visual elements of the conversation and create a new prompt for the image generation AI.
"""}, {"role": "user", "content": f"""Create a prompt for the image generation AI that will make it generate a profile picture for one person based on the following conversation:
{prompt}
"""}],
            temperature=1.2,
            top_p=1.0
        )

        prompt = response.choices[0].message.content
        print(f"💬 GENERATE IMAGE: Prompt: {prompt}")

        # image generation
        response = openai.images.generate(
            model="dall-e-3",  # or "dall-e-2" for the older model
            prompt=prompt,
            size="1024x1024",  # other options: "256x256", "512x512"
            quality="standard",  # or "hd" for dall-e-3
            n=1  # number of images to generate
        )
        
        # The response contains a URL to the generated image
        url = response.data[0].url
        print(f"💬 GENERATE IMAGE: URL: {url}")
        return url
    
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None
