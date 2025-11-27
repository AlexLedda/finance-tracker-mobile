from PIL import Image, ImageDraw, ImageFont
import os

# iOS screenshot dimensions (iPhone 6.5" display - iPhone 14 Pro Max)
WIDTH, HEIGHT = 1284, 2778

def create_base_screen(title, status_bar_color="#4F46E5"):
    """Create base screen with status bar and header for iOS"""
    img = Image.new('RGB', (WIDTH, HEIGHT), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # Status bar (iOS style - taller)
    draw.rectangle([0, 0, WIDTH, 120], fill=status_bar_color)
    
    # Time in center
    try:
        status_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        time_text = "9:41"
        time_bbox = draw.textbbox((0, 0), time_text, font=status_font)
        time_width = time_bbox[2] - time_bbox[0]
        draw.text(((WIDTH - time_width) // 2, 40), time_text, fill='white', font=status_font)
    except:
        pass
    
    # Header with title
    draw.rectangle([0, 120, WIDTH, 320], fill="#4F46E5")
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title centered
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((WIDTH - title_width) // 2, 200), title, fill='white', font=title_font)
    
    return img, draw, title_font, normal_font, small_font


def create_dashboard_ios():
    """Screenshot 1: Dashboard iOS"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Dashboard")
    
    # Balance card
    draw.rounded_rectangle([50, 360, WIDTH-50, 680], radius=25, fill='white')
    draw.text((100, 410), "Saldo Totale", fill='#666', font=small_font)
    draw.text((100, 520), "€ 2,450.00", fill='#4F46E5', font=title_font)
    
    # Income/Expense summary
    y = 730
    draw.rounded_rectangle([50, y, WIDTH//2-25, y+240], radius=25, fill='white')
    draw.rounded_rectangle([WIDTH//2+25, y, WIDTH-50, y+240], radius=25, fill='white')
    
    # Income
    draw.text((100, y+40), "💰 Entrate", fill='#10B981', font=normal_font)
    draw.text((100, y+130), "€ 3,200", fill='#333', font=normal_font)
    
    # Expense
    draw.text((WIDTH//2+75, y+40), "💸 Uscite", fill='#EF4444', font=normal_font)
    draw.text((WIDTH//2+75, y+130), "€ 750", fill='#333', font=normal_font)
    
    # Chart area
    chart_y = 1030
    draw.rounded_rectangle([50, chart_y, WIDTH-50, chart_y+600], radius=25, fill='white')
    draw.text((100, chart_y+40), "Spese per Categoria", fill='#333', font=normal_font)
    
    # Simple chart
    center_x, center_y = WIDTH//2, chart_y+340
    radius = 180
    
    draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], 
                 fill='#4F46E5', outline='white', width=4)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=0, end=120, fill='#10B981', outline='white', width=4)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=120, end=200, fill='#F59E0B', outline='white', width=4)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=200, end=280, fill='#EF4444', outline='white', width=4)
    
    # Legend
    legend_y = chart_y + 540
    colors = [('#4F46E5', 'Altro'), ('#10B981', 'Cibo'), ('#F59E0B', 'Trasporti'), ('#EF4444', 'Shopping')]
    x_offset = 100
    for color, label in colors:
        draw.ellipse([x_offset, legend_y, x_offset+25, legend_y+25], fill=color)
        draw.text((x_offset+35, legend_y-5), label, fill='#666', font=small_font)
        x_offset += 285
    
    # iOS Tab Bar (rounded corners)
    tab_y = HEIGHT - 220
    draw.rounded_rectangle([0, tab_y, WIDTH, HEIGHT], radius=0, fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-35, tab_y+50), item, fill='#4F46E5' if i == 0 else '#999', font=title_font)
    
    img.save('/app/ios-screenshot-1-dashboard.png', 'PNG')
    print("✅ iOS Screenshot 1 (Dashboard) created")


def create_transactions_ios():
    """Screenshot 2: Transactions iOS"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Transazioni")
    
    # Add transaction button
    draw.rounded_rectangle([WIDTH-220, 190, WIDTH-70, 290], radius=20, fill='#10B981')
    draw.text((WIDTH-200, 215), "+ Nuova", fill='white', font=small_font)
    
    # Transactions list
    transactions = [
        ("🍕", "Ristorante", "Cibo", "-€ 45.00", "#EF4444", "Oggi, 13:30"),
        ("⛽", "Benzina", "Trasporti", "-€ 60.00", "#EF4444", "Oggi, 09:15"),
        ("💰", "Stipendio", "Entrate", "+€ 2,800", "#10B981", "26 Nov"),
        ("🛒", "Supermercato", "Cibo", "-€ 85.50", "#EF4444", "25 Nov"),
        ("🎬", "Cinema", "Intrattenimento", "-€ 20.00", "#EF4444", "24 Nov"),
        ("💼", "Freelance", "Entrate", "+€ 400.00", "#10B981", "23 Nov"),
    ]
    
    y = 360
    for emoji, title, category, amount, color, date in transactions:
        draw.rounded_rectangle([50, y, WIDTH-50, y+170], radius=20, fill='white')
        draw.text((100, y+25), emoji, font=title_font)
        draw.text((220, y+30), title, fill='#333', font=normal_font)
        draw.text((220, y+90), category, fill='#999', font=small_font)
        
        amount_bbox = draw.textbbox((0, 0), amount, font=normal_font)
        amount_width = amount_bbox[2] - amount_bbox[0]
        draw.text((WIDTH-amount_width-100, y+30), amount, fill=color, font=normal_font)
        
        date_bbox = draw.textbbox((0, 0), date, font=small_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((WIDTH-date_width-100, y+90), date, fill='#999', font=small_font)
        
        y += 190
    
    # iOS Tab Bar
    tab_y = HEIGHT - 220
    draw.rounded_rectangle([0, tab_y, WIDTH, HEIGHT], radius=0, fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-35, tab_y+50), item, fill='#4F46E5' if i == 1 else '#999', font=title_font)
    
    img.save('/app/ios-screenshot-2-transactions.png', 'PNG')
    print("✅ iOS Screenshot 2 (Transactions) created")


def create_budget_ios():
    """Screenshot 3: Budget iOS"""
    img, draw, title_font, normal_font, small_font = create_base_screen("Budget")
    
    # Monthly budget summary
    draw.rounded_rectangle([50, 360, WIDTH-50, 580], radius=25, fill='white')
    draw.text((100, 410), "Budget Mensile - Novembre", fill='#666', font=small_font)
    draw.text((100, 490), "€ 750 / € 1,000", fill='#4F46E5', font=normal_font)
    
    # Progress bar
    draw.rounded_rectangle([100, 560, WIDTH-100, 610], radius=12, fill='#E5E7EB')
    draw.rounded_rectangle([100, 560, 100 + int((WIDTH-200)*0.75), 610], radius=12, fill='#10B981')
    
    # Category budgets
    categories = [
        ("🍕", "Cibo", "€ 280 / € 400", 0.7, "#10B981"),
        ("🚗", "Trasporti", "€ 180 / € 200", 0.9, "#F59E0B"),
        ("🏠", "Casa", "€ 150 / € 250", 0.6, "#10B981"),
        ("🎮", "Intrattenimento", "€ 140 / € 150", 0.93, "#EF4444"),
    ]
    
    y = 640
    for emoji, category, spent, progress, color in categories:
        draw.rounded_rectangle([50, y, WIDTH-50, y+220], radius=20, fill='white')
        draw.text((100, y+30), emoji, font=title_font)
        draw.text((220, y+45), category, fill='#333', font=normal_font)
        draw.text((220, y+105), spent, fill='#666', font=small_font)
        
        bar_y = y + 160
        draw.rounded_rectangle([220, bar_y, WIDTH-100, bar_y+35], radius=12, fill='#E5E7EB')
        bar_width = int((WIDTH-320) * progress)
        draw.rounded_rectangle([220, bar_y, 220+bar_width, bar_y+35], radius=12, fill=color)
        
        y += 240
    
    # iOS Tab Bar
    tab_y = HEIGHT - 220
    draw.rounded_rectangle([0, tab_y, WIDTH, HEIGHT], radius=0, fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['🏠', '💰', '📊', '⚙️']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        draw.text((x-35, tab_y+50), item, fill='#4F46E5' if i == 2 else '#999', font=title_font)
    
    img.save('/app/ios-screenshot-3-budget.png', 'PNG')
    print("✅ iOS Screenshot 3 (Budget) created")


# Create all iOS screenshots
print("🎨 Creating iOS screenshots for Finance Tracker...")
create_dashboard_ios()
create_transactions_ios()
create_budget_ios()
print("\n✅ All iOS screenshots created successfully!")
print("\nFiles created:")
print("  - /app/ios-screenshot-1-dashboard.png (1284x2778)")
print("  - /app/ios-screenshot-2-transactions.png (1284x2778)")
print("  - /app/ios-screenshot-3-budget.png (1284x2778)")
