from PIL import Image, ImageDraw, ImageFont
import os

# Create a 1024x500 image
width, height = 1024, 500
image = Image.new('RGB', (width, height), color='#4F46E5')

# Create gradient background
draw = ImageDraw.Draw(image)

# Draw gradient manually
for y in range(height):
    # Interpolate between colors
    ratio = y / height
    r = int(79 + (124 - 79) * ratio)
    g = int(70 + (58 - 70) * ratio)
    b = int(229 + (237 - 229) * ratio)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Try to use a font, fallback to default if not available
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    feature_font = ImageFont.load_default()

# Draw title
title = "Finance Tracker"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2
draw.text((title_x, 120), title, fill='white', font=title_font)

# Draw subtitle
subtitle = "Gestisci le tue finanze con facilità"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, 220), subtitle, fill='white', font=subtitle_font)

# Draw features
features = ["💰 Transazioni", "📊 Budget", "🎯 Obiettivi"]
feature_y = 320
spacing = width // (len(features) + 1)

for i, feature in enumerate(features):
    feature_bbox = draw.textbbox((0, 0), feature, font=feature_font)
    feature_width = feature_bbox[2] - feature_bbox[0]
    feature_x = spacing * (i + 1) - feature_width // 2
    draw.text((feature_x, feature_y), feature, fill='white', font=feature_font)

# Add decorative elements
draw.rectangle([50, 400, 974, 405], fill='white', outline='white')

# Save the image
image.save('/app/feature-graphic.png', 'PNG', quality=95)
print("Feature graphic created successfully at /app/feature-graphic.png")
