from PIL import Image, ImageDraw, ImageFont
import os

# Screenshot dimensions (standard Android phone)
WIDTH, HEIGHT = 1080, 2340

def create_base_screen(title, status_bar_color="#4F46E5"):
    """Create base screen with status bar and header"""
    img = Image.new('RGB', (WIDTH, HEIGHT), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([0, 0, WIDTH, 100], fill=status_bar_color)
    
    # Header with title
    draw.rectangle([0, 100, WIDTH, 280], fill="#4F46E5")
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title centered
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((WIDTH - title_width) // 2, 170), title, fill='white', font=title_font)
    
    return img, draw, title_font, normal_font, small_font


def create_dashboard():
    """Screenshot 1: Dashboard"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Dashboard")
    
    # Balance card
    draw.rounded_rectangle([40, 320, WIDTH-40, 580], radius=20, fill='white')
    draw.text((80, 360), "Saldo Totale", fill='#666', font=small_font)
    draw.text((80, 440), "€ 2,450.00", fill='#4F46E5', font=title_font)
    
    # Income/Expense summary
    y = 620
    draw.rounded_rectangle([40, y, WIDTH//2-20, y+200], radius=20, fill='white')
    draw.rounded_rectangle([WIDTH//2+20, y, WIDTH-40, y+200], radius=20, fill='white')
    
    # Income
    draw.text((80, y+30), "💰 Entrate", fill='#10B981', font=normal_font)
    draw.text((80, y+100), "€ 3,200", fill='#333', font=normal_font)
    
    # Expense
    draw.text((WIDTH//2+60, y+30), "💸 Uscite", fill='#EF4444', font=normal_font)
    draw.text((WIDTH//2+60, y+100), "€ 750", fill='#333', font=normal_font)
    
    # Chart area (simplified pie chart representation)
    chart_y = 860
    draw.rounded_rectangle([40, chart_y, WIDTH-40, chart_y+500], radius=20, fill='white')
    draw.text((80, chart_y+30), "Spese per Categoria", fill='#333', font=normal_font)
    
    # Simple chart representation
    center_x, center_y = WIDTH//2, chart_y+280
    radius = 150
    
    # Draw pie slices (simplified as circles)
    draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], 
                 fill='#4F46E5', outline='white', width=3)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=0, end=120, fill='#10B981', outline='white', width=3)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=120, end=200, fill='#F59E0B', outline='white', width=3)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=200, end=280, fill='#EF4444', outline='white', width=3)
    
    # Legend
    legend_y = chart_y + 450
    colors = [('#4F46E5', 'Altro'), ('#10B981', 'Cibo'), ('#F59E0B', 'Trasporti'), ('#EF4444', 'Shopping')]
    x_offset = 80
    for color, label in colors:
        draw.ellipse([x_offset, legend_y, x_offset+20, legend_y+20], fill=color)
        draw.text((x_offset+30, legend_y-5), label, fill='#666', font=small_font)
        x_offset += 240
    
    # Bottom navigation
    draw.rectangle([0, HEIGHT-180, WIDTH, HEIGHT], fill='white')
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-30, HEIGHT-130), item, fill='#4F46E5' if i == 0 else '#999', font=title_font)
    
    img.save('/app/screenshot-1-dashboard.png', 'PNG')
    print("✅ Screenshot 1 (Dashboard) created")


def create_transactions():
    """Screenshot 2: Transactions"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Transazioni")
    
    # Add transaction button
    draw.rounded_rectangle([WIDTH-180, 160, WIDTH-60, 240], radius=15, fill='#10B981')
    draw.text((WIDTH-160, 180), "+ Nuova", fill='white', font=small_font)
    
    # Transactions list
    transactions = [
        ("🍕", "Ristorante", "Cibo", "-€ 45.00", "#EF4444", "Oggi, 13:30"),
        ("⛽", "Benzina", "Trasporti", "-€ 60.00", "#EF4444", "Oggi, 09:15"),
        ("💰", "Stipendio", "Entrate", "+€ 2,800", "#10B981", "26 Nov"),
        ("🛒", "Supermercato", "Cibo", "-€ 85.50", "#EF4444", "25 Nov"),
        ("🎬", "Cinema", "Intrattenimento", "-€ 20.00", "#EF4444", "24 Nov"),
        ("💼", "Freelance", "Entrate", "+€ 400.00", "#10B981", "23 Nov"),
    ]
    
    y = 320
    for emoji, title, category, amount, color, date in transactions:
        # Transaction card
        draw.rounded_rectangle([40, y, WIDTH-40, y+140], radius=15, fill='white')
        
        # Emoji icon
        draw.text((80, y+20), emoji, font=title_font)
        
        # Title and category
        draw.text((180, y+25), title, fill='#333', font=normal_font)
        draw.text((180, y+75), category, fill='#999', font=small_font)
        
        # Amount (right aligned)
        amount_bbox = draw.textbbox((0, 0), amount, font=normal_font)
        amount_width = amount_bbox[2] - amount_bbox[0]
        draw.text((WIDTH-amount_width-80, y+25), amount, fill=color, font=normal_font)
        
        # Date
        date_bbox = draw.textbbox((0, 0), date, font=small_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((WIDTH-date_width-80, y+75), date, fill='#999', font=small_font)
        
        y += 160
    
    # Bottom navigation
    draw.rectangle([0, HEIGHT-180, WIDTH, HEIGHT], fill='white')
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-30, HEIGHT-130), item, fill='#4F46E5' if i == 1 else '#999', font=title_font)
    
    img.save('/app/screenshot-2-transactions.png', 'PNG')
    print("✅ Screenshot 2 (Transactions) created")


def create_budget():
    """Screenshot 3: Budget"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Budget")
    
    # Monthly budget summary
    draw.rounded_rectangle([40, 320, WIDTH-40, 500], radius=20, fill='white')
    draw.text((80, 360), "Budget Mensile - Novembre", fill='#666', font=small_font)
    draw.text((80, 420), "€ 750 / € 1,000", fill='#4F46E5', font=normal_font)
    
    # Progress bar
    draw.rounded_rectangle([80, 480, WIDTH-80, 520], radius=10, fill='#E5E7EB')
    draw.rounded_rectangle([80, 480, 80 + int((WIDTH-160)*0.75), 520], radius=10, fill='#10B981')
    
    # Category budgets
    categories = [
        ("🍕", "Cibo", "€ 280 / € 400", 0.7, "#10B981"),
        ("🚗", "Trasporti", "€ 180 / € 200", 0.9, "#F59E0B"),
        ("🏠", "Casa", "€ 150 / € 250", 0.6, "#10B981"),
        ("🎮", "Intrattenimento", "€ 140 / € 150", 0.93, "#EF4444"),
    ]
    
    y = 550
    for emoji, category, spent, progress, color in categories:
        # Category card
        draw.rounded_rectangle([40, y, WIDTH-40, y+180], radius=15, fill='white')
        
        # Emoji and category
        draw.text((80, y+25), emoji, font=title_font)
        draw.text((180, y+35), category, fill='#333', font=normal_font)
        
        # Amount
        draw.text((180, y+85), spent, fill='#666', font=small_font)
        
        # Progress bar
        bar_y = y + 130
        draw.rounded_rectangle([180, bar_y, WIDTH-80, bar_y+30], radius=10, fill='#E5E7EB')
        bar_width = int((WIDTH-260) * progress)
        draw.rounded_rectangle([180, bar_y, 180+bar_width, bar_y+30], radius=10, fill=color)
        
        y += 200
    
    # Bottom navigation
    draw.rectangle([0, HEIGHT-180, WIDTH, HEIGHT], fill='white')
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-30, HEIGHT-130), item, fill='#4F46E5' if i == 2 else '#999', font=title_font)
    
    img.save('/app/screenshot-3-budget.png', 'PNG')
    print("✅ Screenshot 3 (Budget) created")


def create_goals():
    """Screenshot 4: Goals"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Obiettivi")
    
    # Goals list
    goals = [
        ("🏖️", "Vacanza Estate", "€ 1,200 / € 2,000", 0.6, "#4F46E5"),
        ("💻", "Nuovo Laptop", "€ 450 / € 1,500", 0.3, "#10B981"),
        ("🚗", "Auto Nuova", "€ 3,000 / € 10,000", 0.3, "#F59E0B"),
        ("🏠", "Fondo Emergenza", "€ 2,500 / € 5,000", 0.5, "#10B981"),
    ]
    
    y = 320
    for emoji, goal, saved, progress, color in goals:
        # Goal card
        draw.rounded_rectangle([40, y, WIDTH-40, y+220], radius=20, fill='white')
        
        # Emoji
        draw.text((80, y+30), emoji, font=title_font)
        
        # Goal name
        draw.text((200, y+45), goal, fill='#333', font=normal_font)
        
        # Amount saved
        draw.text((80, y+110), saved, fill='#666', font=small_font)
        
        # Progress bar
        bar_y = y + 160
        draw.rounded_rectangle([80, bar_y, WIDTH-80, bar_y+35], radius=12, fill='#E5E7EB')
        bar_width = int((WIDTH-160) * progress)
        draw.rounded_rectangle([80, bar_y, 80+bar_width, bar_y+35], radius=12, fill=color)
        
        # Percentage
        percentage = f"{int(progress*100)}%"
        perc_bbox = draw.textbbox((0, 0), percentage, font=small_font)
        perc_width = perc_bbox[2] - perc_bbox[0]
        draw.text((WIDTH-perc_width-100, y+45), percentage, fill=color, font=normal_font)
        
        y += 250
    
    # Add goal button
    button_y = y + 20
    draw.rounded_rectangle([40, button_y, WIDTH-40, button_y+120], radius=15, fill='#4F46E5')
    plus_text = "+ Nuovo Obiettivo"
    plus_bbox = draw.textbbox((0, 0), plus_text, font=normal_font)
    plus_width = plus_bbox[2] - plus_bbox[0]
    draw.text(((WIDTH-plus_width)//2, button_y+40), plus_text, fill='white', font=normal_font)
    
    # Bottom navigation
    draw.rectangle([0, HEIGHT-180, WIDTH, HEIGHT], fill='white')
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-30, HEIGHT-130), item, fill='#4F46E5' if i == 2 else '#999', font=title_font)
    
    img.save('/app/screenshot-4-goals.png', 'PNG')
    print("✅ Screenshot 4 (Goals) created")


# Create all screenshots
print("🎨 Creating professional screenshots for Finance Tracker...")
create_dashboard()
create_transactions()
create_budget()
create_goals()
print("\n✅ All screenshots created successfully!")
print("\nFiles created:")
print("  - /app/screenshot-1-dashboard.png")
print("  - /app/screenshot-2-transactions.png")
print("  - /app/screenshot-3-budget.png")
print("  - /app/screenshot-4-goals.png")
