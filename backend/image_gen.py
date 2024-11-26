
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from threading import Lock


BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BACKEND_DIR, 'assets')

# Parameters for the chat image
width, height = 540, 960
background_color = "#121212"  # Lightest grey in Pillow's web-safe colors
sender_color = "#1d1d1d"
receiver_color = "#2c2c2c"
text_color = "white"
timestamp_color = "white"
date_divider_color = "orange"

action_bar_height = 80  # Height of the top bar
action_bar_color = "black"
action_bar_text_color = "white"
action_bar_text_size = 22
action_bar_padding = 10
icon_size = (40, 40)

text_input_bottom_bar_height = 100
text_input_bottom_bar_color = "#1d1d1d"

# Font settings
# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Replace with your font path
font_size = 16
timestamp_font_size = 12

# Load fonts
font = ImageFont.load_default().font_variant(size=font_size)
timestamp_font = ImageFont.load_default().font_variant(size=timestamp_font_size)

# Initialize image
img = Image.new("RGB", (width, height), color=background_color)
draw = ImageDraw.Draw(img)

def verify_assets():
    """Verify that all required assets are available."""
    required_assets = ['profile.png']
    
    for asset in required_assets:
        asset_path = os.path.join(ASSETS_DIR, asset)
        if not os.path.exists(asset_path):
            raise FileNotFoundError(
                f"Required asset not found: {asset_path}\n"
                f"Please ensure all assets are in the {ASSETS_DIR} directory."
            )
def draw_text_input_bar(draw, img):
    # Draw the background bar
    draw.rectangle(
        [(0, height - text_input_bottom_bar_height), (width, height)],
        fill=text_input_bottom_bar_color
    )
    
    # Draw rounded search bar
    search_bar_padding = 10
    search_bar_height = 45
    search_bar_y = height - (text_input_bottom_bar_height // 2) - (search_bar_height // 2)
    
    # Draw rounded rectangle for search bar
    draw.rounded_rectangle(
        [
            (search_bar_padding, search_bar_y),
            (width - search_bar_padding, search_bar_y + search_bar_height)
        ],
        radius=22,
        fill="#1d1d1d"  # Slightly lighter than background
    )
    
    # Add placeholder text
    placeholder_text = "Type something..."
    placeholder_font = ImageFont.load_default().font_variant(size=18)
    text_bbox = draw.textbbox((0, 0), placeholder_text, font=placeholder_font)
    text_height = text_bbox[3] - text_bbox[1]
    text_y = search_bar_y + (search_bar_height - text_height) // 2
    
    draw.text(
        (search_bar_padding + 45, text_y),  # Extra padding for X icon
        placeholder_text,
        fill="#808080",  # Gray color for placeholder
        font=placeholder_font
    )
    
    # Add microphone icon on right (you'll need to implement this with an actual icon)
    mic_size = 20
    mic_x = width - search_bar_padding - mic_size - 10
    mic_y = search_bar_y + (search_bar_height - mic_size) // 2
    draw.ellipse((mic_x - mic_size, mic_y - mic_size, mic_x + mic_size, mic_y + mic_size), fill="white")
    return search_bar_y

def draw_action_bar(draw, img, name, file_name):
    draw.rectangle(
        [(0, 0), (width, action_bar_height)],
        fill=action_bar_color
    )
    
    # Add the icon with better error handling
    icon_path = os.path.join(ASSETS_DIR, file_name)
    try:
        if not os.path.exists(icon_path):
            print(f"❌ Icon not found at: {icon_path}")
            raise FileNotFoundError(f"Icon not found at: {icon_path}")
            
        icon = Image.open(icon_path)
        
        # Resize icon while maintaining aspect ratio
        icon.thumbnail(icon_size)
        # Calculate vertical position to center the icon
        icon_y = (action_bar_height - icon.height) // 2
        
        # Paste the icon (handles transparency if PNG)
        if icon.mode == 'RGBA':
            img.paste(icon, (action_bar_padding, icon_y), icon)
        else:
            img.paste(icon, (action_bar_padding, icon_y))
            
        text_start_x = action_bar_padding + icon_size[0] + action_bar_padding
        
    except Exception as e:
        print(f"❌ Error loading icon: {str(e)}")
        # Fallback: start text from the left padding if icon fails
        text_start_x = action_bar_padding
    
    # Draw the action bar text
    text_bbox = draw.textbbox((0, 0), name, font=ImageFont.load_default().font_variant(size=action_bar_text_size))
    text_height = text_bbox[3] - text_bbox[1]
    text_y = (action_bar_height - text_height) // 2  # Vertically center
    
    draw.text(
        (text_start_x, text_y),
        name,
        fill=action_bar_text_color,
        font=ImageFont.load_default().font_variant(size=action_bar_text_size)
    )

# Function to draw a chat bubble
def draw_bubble(
        draw, 
        img, 
        item, 
        sender=True, 
        timestamp="", 
        status=None, 
        y_position=0, 
        name="Siri", 
        file_name="",
        search_bar_y=0
    ):
    
    # Determine bubble size
    padding = 20
    max_text_width = 400

    text = item["message"]
    wrapped_text = textwrap.fill(text, width=43)

    # Deprecated textsize replace with textbbox
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    bubble_width = min(max_text_width, text_width + 20)
    bubble_height = text_height + 40

    if (y_position + bubble_height + padding) > search_bar_y:
        return y_position + bubble_height + padding, item
    
    # Set position and color
    x_position = padding if sender else width - bubble_width - padding
    bubble_color = sender_color if sender else receiver_color

    # Draw bubble
    draw.rounded_rectangle(
        (x_position, y_position, x_position + bubble_width, y_position + bubble_height), 
        radius=15, 
        fill=bubble_color
    )

    # Draw text with consistent padding
    text_padding = 10
    draw.multiline_text(
        (x_position + text_padding, y_position + text_padding), 
        wrapped_text, 
        fill=text_color, 
        font=font
    )

    # Draw timestamp
    timestamp_position = (
        x_position + bubble_width - 65, 
        y_position + bubble_height - 20
    )
    draw.text(
        timestamp_position, 
        timestamp, 
        fill=timestamp_color, 
        font=timestamp_font
    )

    # Draw status icon (e.g., check mark for read status)
    # if not sender:
    #     status_position = (x_position + bubble_width - 10, y_position + bubble_height - 20)
    #     draw.text(
    #         status_position, 
    #         "\u2713\u2713", 
    #         fill=timestamp_color, 
    #         font=timestamp_font
    #     )

    # Return the new y_position for the next message
    return y_position + bubble_height + padding, None

def draw_conversation(conversation_data, name, file_name, page=1, images_list=None):
  if images_list is None:
    images_list = []

  current_y = 50 + action_bar_height  # Starting y position

  # Initialize single image for complete conversation
  in_img = Image.new("RGB", (width, height), color=background_color)
  in_draw = ImageDraw.Draw(in_img)

  draw_action_bar(in_draw, in_img, name, file_name)
  search_bar_y = draw_text_input_bar(in_draw, in_img)
  
  # Draw complete conversation
  for i, item in enumerate(conversation_data):
      sender = item["speaker"] == "Person 1"
      current_y, remaining_item = draw_bubble(
          in_draw,
          in_img, 
          item,
          sender=sender,
          timestamp=item["timestamp"],
          y_position=current_y,
          name=name,
          file_name=file_name,
          search_bar_y=search_bar_y
      )
        
      if remaining_item:
        images_list.append(in_img)
        remaining_conversation = conversation_data[i:]
        return draw_conversation(
            remaining_conversation, 
            name, 
            file_name, 
            page + 1, 
            images_list
        )
         
  images_list.append(in_img)
  return images_list
