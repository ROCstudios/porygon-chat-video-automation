from PIL import Image, ImageDraw, ImageFont
import textwrap

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
action_bar_padding = 10
icon_size = (40, 40)
icon_path = "backend/profile.png"

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

def draw_action_bar(draw, name):
    print("✍️ DRAW ACTION BAR: Drawing action bar")
    draw.rectangle(
        [(0, 0), (width, action_bar_height)],
        fill=action_bar_color
    )
    
    # Add the icon
    try:
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
            
        # Calculate text position after icon
        text_start_x = action_bar_padding + icon_size[0] + action_bar_padding
    except FileNotFoundError:
        # If no icon is found, start text from the left padding
        text_start_x = action_bar_padding
    
    # Draw the action bar text
    text_bbox = draw.textbbox((0, 0), name)
    text_height = text_bbox[3] - text_bbox[1]
    text_y = (action_bar_height - text_height) // 2  # Vertically center
    
    draw.text(
        (text_start_x, text_y),
        name,
        fill=action_bar_text_color
    )

# Function to draw a chat bubble
def draw_bubble(draw, text, sender=True, timestamp="", status=None, y_position=0, name="Siri"):
    padding = 20

    # Determine bubble size
    max_text_width = 400
    wrapped_text = textwrap.fill(text, width=43)

    # Deprecated textsize replace with textbbox
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    bubble_width = min(max_text_width, text_width + 20)
    bubble_height = text_height + 40

    # Set position and color
    x_position = padding if sender else width - bubble_width - padding
    bubble_color = sender_color if sender else receiver_color

    #action bar
    draw_action_bar(draw, name)

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
    return y_position + bubble_height + padding

# Draw the chat conversation
def draw_conversation(conversation_data, name):
  print(f"✍️ DRAW CONVERSATION: Drawing conversation with {len(conversation_data)} turns")

  images_list = []
  current_y = 50 + action_bar_height  # Starting y position

  for i in range(len(conversation_data)):
      # Initialize new image for each progressive conversation
      in_img = Image.new("RGB", (width, height), color=background_color)
      in_draw = ImageDraw.Draw(in_img)
      
      current_y = 50 + action_bar_height  # Reset starting y position
      
      # Draw conversation up to current message
      for item in conversation_data[:i+1]:
          sender = item["speaker"] == "Person 1"
          current_y = draw_bubble(
              in_draw, 
              item["message"], 
              sender=sender, 
              timestamp=item["timestamp"], 
              y_position=current_y,
              name=name
          )
          
      images_list.append(in_img)

  print(f"✍️ DRAW CONVERSATION: Images list: {images_list}")
  return images_list
