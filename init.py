import argparse

from image_gen import draw_conversation
from movie_gen import create_video
from convo_gen import generate_conversation

def main():
    parser = argparse.ArgumentParser(description='Generate conversation videos')
    parser.add_argument('--topic', type=str, required=True, help='Topic for the conversation')
    parser.add_argument('--turns', type=int, default=5, help='Number of conversation turns (default: 5)')
    
    # Parse arguments
    args = parser.parse_args()

    conversation_data = generate_conversation(args.topic, args.turns)
    images_list = draw_conversation(conversation_data)
    video_destination = create_video(images_list)

if __name__ == "__main__":
    main()
