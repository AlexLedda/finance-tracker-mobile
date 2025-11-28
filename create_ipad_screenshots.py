from PIL import Image, ImageDraw, ImageFont
import os

# iPad Pro 12.9" dimensions (3rd gen and later)
WIDTH, HEIGHT = 2048, 2732

def create_base_screen_ipad(title, status_bar_color="#4F46E5"):
    """Create base screen with status bar and header for iPad"""
    img = Image.new('RGB', (WIDTH, HEIGHT), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # Status bar (iPad style)
    draw.rectangle([0, 0, WIDTH, 80], fill=status_bar_color)
    
    # Time in center
    try:
        status_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        time_text = "9:41"
        time_bbox = draw.textbbox((0, 0), time_text, font=status_font)
        time_width = time_bbox[2] - time_bbox[0]
        draw.text(((WIDTH - time_width) // 2, 30), time_text, fill='white', font=status_font)
    except:
        pass
    
    # Header with title
    draw.rectangle([0, 80, WIDTH, 240], fill="#4F46E5")
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 56)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title centered
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((WIDTH - title_width) // 2, 140), title, fill='white', font=title_font)
    
    return img, draw, title_font, normal_font, small_font


def create_dashboard_ipad():
    """Screenshot 1: Dashboard iPad"""
    img, draw, title_font, normal_font, small_font = create_base_screen_ipad("Dashboard")
    
    # Two column layout for iPad
    col1_x = 80
    col2_x = WIDTH // 2 + 40
    col_width = WIDTH // 2 - 120
    
    # Balance card (top, full width)
    draw.rounded_rectangle([80, 300, WIDTH-80, 580], radius=30, fill='white')
    draw.text((140, 360), "Saldo Totale", fill='#666', font=small_font)
    draw.text((140, 460), "€ 2,450.00", fill='#4F46E5', font=title_font)
    
    # Income card (left)
    y = 640
    draw.rounded_rectangle([col1_x, y, col1_x+col_width, y+280], radius=30, fill='white')
    draw.text((col1_x+60, y+50), "Entrate", fill='#10B981', font=normal_font)
    draw.text((col1_x+60, y+150), "€ 3,200", fill='#333', font=title_font)
    
    # Expense card (right)
    draw.rounded_rectangle([col2_x, y, col2_x+col_width, y+280], radius=30, fill='white')
    draw.text((col2_x+60, y+50), "Uscite", fill='#EF4444', font=normal_font)
    draw.text((col2_x+60, y+150), "€ 750", fill='#333', font=title_font)
    
    # Chart area (full width)
    chart_y = 980
    draw.rounded_rectangle([80, chart_y, WIDTH-80, chart_y+800], radius=30, fill='white')
    draw.text((140, chart_y+50), "Spese per Categoria", fill='#333', font=normal_font)
    
    # Larger chart for iPad
    center_x, center_y = WIDTH//2, chart_y+450
    radius = 250
    
    draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], 
                 fill='#4F46E5', outline='white', width=5)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=0, end=120, fill='#10B981', outline='white', width=5)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=120, end=200, fill='#F59E0B', outline='white', width=5)
    draw.pieslice([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                  start=200, end=280, fill='#EF4444', outline='white', width=5)
    
    # Legend (centered)
    legend_y = chart_y + 720
    colors = [('#4F46E5', 'Altro'), ('#10B981', 'Cibo'), ('#F59E0B', 'Trasporti'), ('#EF4444', 'Shopping')]
    total_legend_width = len(colors) * 350
    start_x = (WIDTH - total_legend_width) // 2
    
    for i, (color, label) in enumerate(colors):
        x = start_x + i * 350
        draw.ellipse([x, legend_y, x+30, legend_y+30], fill=color)
        draw.text((x+40, legend_y-5), label, fill='#666', font=small_font)
    
    # Bottom tab bar
    tab_y = HEIGHT - 150
    draw.rectangle([0, tab_y, WIDTH, HEIGHT], fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['Dashboard', 'Transazioni', 'Budget', 'Impostazioni']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        bbox = draw.textbbox((0, 0), item, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, tab_y+50), item, fill='#4F46E5' if i == 0 else '#999', font=small_font)
    
    img.save('/app/ipad-screenshot-1-dashboard.png', 'PNG')
    print("✅ iPad Screenshot 1 (Dashboard) created")


def create_transactions_ipad():
    """Screenshot 2: Transactions iPad"""
    img, draw, title_font, normal_font, small_font = create_base_screen_ipad("Transazioni")
    
    # Add transaction button
    draw.rounded_rectangle([WIDTH-320, 130, WIDTH-100, 230], radius=25, fill='#10B981')
    draw.text((WIDTH-300, 165), "+ Nuova", fill='white', font=normal_font)
    
    # Two column layout for transactions
    col1_x = 80
    col2_x = WIDTH // 2 + 40
    col_width = WIDTH // 2 - 120
    
    transactions_col1 = [
        ("Ristorante", "Cibo", "-€ 45.00", "#EF4444", "Oggi, 13:30"),
        ("Benzina", "Trasporti", "-€ 60.00", "#EF4444", "Oggi, 09:15"),
        ("Stipendio", "Entrate", "+€ 2,800", "#10B981", "26 Nov"),
    ]
    
    transactions_col2 = [
        ("Supermercato", "Cibo", "-€ 85.50", "#EF4444", "25 Nov"),
        ("Cinema", "Intrattenimento", "-€ 20.00", "#EF4444", "24 Nov"),
        ("Freelance", "Entrate", "+€ 400.00", "#10B981", "23 Nov"),
    ]
    
    y = 300
    for title, category, amount, color, date in transactions_col1:
        draw.rounded_rectangle([col1_x, y, col1_x+col_width, y+200], radius=25, fill='white')
        draw.text((col1_x+60, y+30), title, fill='#333', font=normal_font)
        draw.text((col1_x+60, y+90), category, fill='#999', font=small_font)
        
        amount_bbox = draw.textbbox((0, 0), amount, font=normal_font)
        amount_width = amount_bbox[2] - amount_bbox[0]
        draw.text((col1_x+col_width-amount_width-60, y+30), amount, fill=color, font=normal_font)
        
        date_bbox = draw.textbbox((0, 0), date, font=small_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((col1_x+col_width-date_width-60, y+90), date, fill='#999', font=small_font)
        
        y += 230
    
    y = 300
    for title, category, amount, color, date in transactions_col2:
        draw.rounded_rectangle([col2_x, y, col2_x+col_width, y+200], radius=25, fill='white')
        draw.text((col2_x+60, y+30), title, fill='#333', font=normal_font)
        draw.text((col2_x+60, y+90), category, fill='#999', font=small_font)
        
        amount_bbox = draw.textbbox((0, 0), amount, font=normal_font)
        amount_width = amount_bbox[2] - amount_bbox[0]
        draw.text((col2_x+col_width-amount_width-60, y+30), amount, fill=color, font=normal_font)
        
        date_bbox = draw.textbbox((0, 0), date, font=small_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((col2_x+col_width-date_width-60, y+90), date, fill='#999', font=small_font)
        
        y += 230
    
    # Bottom tab bar
    tab_y = HEIGHT - 150
    draw.rectangle([0, tab_y, WIDTH, HEIGHT], fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['Dashboard', 'Transazioni', 'Budget', 'Impostazioni']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        bbox = draw.textbbox((0, 0), item, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, tab_y+50), item, fill='#4F46E5' if i == 1 else '#999', font=small_font)
    
    img.save('/app/ipad-screenshot-2-transactions.png', 'PNG')
    print("✅ iPad Screenshot 2 (Transactions) created")


def create_budget_ipad():
    """Screenshot 3: Budget iPad"""
    img, draw, title_font, normal_font, small_font = create_base_screen_ipad("Budget")
    
    # Monthly budget summary (full width)
    draw.rounded_rectangle([80, 300, WIDTH-80, 540], radius=30, fill='white')
    draw.text((140, 350), "Budget Mensile - Novembre", fill='#666', font=small_font)
    draw.text((140, 430), "€ 750 / € 1,000", fill='#4F46E5', font=normal_font)
    
    # Progress bar
    draw.rounded_rectangle([140, 510, WIDTH-140, 560], radius=15, fill='#E5E7EB')
    draw.rounded_rectangle([140, 510, 140 + int((WIDTH-280)*0.75), 560], radius=15, fill='#10B981')
    
    # Two column layout for categories
    col1_x = 80
    col2_x = WIDTH // 2 + 40
    col_width = WIDTH // 2 - 120
    
    categories_col1 = [
        ("Cibo", "€ 280 / € 400", 0.7, "#10B981"),
        ("Trasporti", "€ 180 / € 200", 0.9, "#F59E0B"),
    ]
    
    categories_col2 = [
        ("Casa", "€ 150 / € 250", 0.6, "#10B981"),
        ("Intrattenimento", "€ 140 / € 150", 0.93, "#EF4444"),
    ]
    
    y = 620
    for category, spent, progress, color in categories_col1:
        draw.rounded_rectangle([col1_x, y, col1_x+col_width, y+260], radius=25, fill='white')
        draw.text((col1_x+60, y+40), category, fill='#333', font=normal_font)
        draw.text((col1_x+60, y+110), spent, fill='#666', font=small_font)
        
        bar_y = y + 190
        draw.rounded_rectangle([col1_x+60, bar_y, col1_x+col_width-60, bar_y+40], radius=15, fill='#E5E7EB')
        bar_width = int((col_width-120) * progress)
        draw.rounded_rectangle([col1_x+60, bar_y, col1_x+60+bar_width, bar_y+40], radius=15, fill=color)
        
        y += 300
    
    y = 620
    for category, spent, progress, color in categories_col2:
        draw.rounded_rectangle([col2_x, y, col2_x+col_width, y+260], radius=25, fill='white')
        draw.text((col2_x+60, y+40), category, fill='#333', font=normal_font)
        draw.text((col2_x+60, y+110), spent, fill='#666', font=small_font)
        
        bar_y = y + 190
        draw.rounded_rectangle([col2_x+60, bar_y, col2_x+col_width-60, bar_y+40], radius=15, fill='#E5E7EB')
        bar_width = int((col_width-120) * progress)
        draw.rounded_rectangle([col2_x+60, bar_y, col2_x+60+bar_width, bar_y+40], radius=15, fill=color)
        
        y += 300
    
    # Bottom tab bar
    tab_y = HEIGHT - 150
    draw.rectangle([0, tab_y, WIDTH, HEIGHT], fill='white')
    draw.rectangle([0, tab_y, WIDTH, tab_y+2], fill='#E5E5E5')
    
    nav_items = ['Dashboard', 'Transazioni', 'Budget', 'Impostazioni']
    nav_width = WIDTH // len(nav_items)
    for i, item in enumerate(nav_items):
        x = i * nav_width + nav_width // 2
        bbox = draw.textbbox((0, 0), item, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, tab_y+50), item, fill='#4F46E5' if i == 2 else '#999', font=small_font)
    
    img.save('/app/ipad-screenshot-3-budget.png', 'PNG')
    print("✅ iPad Screenshot 3 (Budget) created")


# Create all iPad screenshots
print("🎨 Creating iPad screenshots for Finance Tracker...")
create_dashboard_ipad()
create_transactions_ipad()
create_budget_ipad()
print("\n✅ All iPad screenshots created successfully!")
print("\nFiles created:")
print("  - /app/ipad-screenshot-1-dashboard.png (2048x2732)")
print("  - /app/ipad-screenshot-2-transactions.png (2048x2732)")
print("  - /app/ipad-screenshot-3-budget.png (2048x2732)")
