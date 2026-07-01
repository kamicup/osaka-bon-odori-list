import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 1. データの読み込みとパース
report_path = '/Users/yoshikazuhashimoto/tmp/2026/bonodori_report_2026.md'
if not os.path.exists(report_path):
    report_path = '/Users/yoshikazuhashimoto/.gemini/antigravity-cli/brain/29c87b03-b41e-4f3a-9939-e5f07924f889/2026/bonodori_report_2026.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

def parse_date(date_str):
    months_days = []
    date_str = re.sub(r'^\d+年', '', date_str)
    matches = re.findall(r'(\d+)月\s*(\d+)日', date_str)
    for m, d in matches:
        months_days.append((int(m), int(d)))
    return months_days

events = []
table_match = re.search(r'## 1\. 信頼できる情報源に基づく盆踊り一覧.*?\n(.*?)\n\n## 2\.', content, re.DOTALL)
if table_match:
    table_text = table_match.group(1)
    lines = table_text.strip().split('\n')
    for line in lines:
        if line.startswith('|') and not line.startswith('| ---') and not line.startswith('| 開催年月日'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 8:
                date_str = parts[0]
                name = parts[1]
                place = parts[2]
                city = parts[3]
                ward = parts[4]
                performer = parts[5]
                notes = parts[7]
                
                dates = parse_date(date_str)
                events.append({
                    'dates': dates,
                    'name': name.replace('（盆踊り実施）', '').replace('（盆踊り等を実施）', ''),
                    'place': place,
                    'ward': ward,
                    'notes': notes
                })

# 日付ごとのマップ
calendar_events = {7: {}, 8: {}}
for ev in events:
    for m, d in ev['dates']:
        if m in [7, 8]:
            if d not in calendar_events[m]:
                calendar_events[m][d] = []
            calendar_events[m][d].append(ev)

# フォントの設定
font_candidates = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf"
]
font_path = None
for f in font_candidates:
    if os.path.exists(f):
        font_path = f
        break

def get_font(size, bold=False):
    if font_path:
        return ImageFont.truetype(font_path, size, index=1 if bold else 0)
    else:
        return ImageFont.load_default()

# 2. 超高精細縦長カレンダー描画
def generate_ultra_calendar(month, title_text, output_filename, print_mode=False):
    width = 3000
    height = 4800
    
    # 背景のカラー定義
    if print_mode:
        base = Image.new('RGB', (width, height), '#FFFFFF')
        draw = ImageDraw.Draw(base)
    else:
        base = Image.new('RGB', (width, height), '#0A0E29')
        draw = ImageDraw.Draw(base)
        for y in range(height):
            r = int(0x05 + (0x1C - 0x05) * (y / height))
            g = int(0x0A + (0x10 - 0x0A) * (y / height))
            b = int(0x20 + (0x35 - 0x20) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
            
    # 光彩エフェクトの描画 (通常版のみ)
    if not print_mode:
        glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        for i in range(20):
            tx = 75 + i * 150
            ty = 220 + (i % 2) * 20
            for r_size in range(80, 0, -5):
                alpha = int(100 * (1 - r_size / 80))
                glow_draw.ellipse([tx - r_size, ty - r_size, tx + r_size, ty + r_size], fill=(255, 140, 0, alpha))
        glow_blurred = glow.filter(ImageFilter.GaussianBlur(30))
        base.paste(glow_blurred, (0, 0), glow_blurred)
        
    draw = ImageDraw.Draw(base)
    
    # 提灯本体の描画
    for i in range(20):
        tx = 75 + i * 150
        ty = 220 + (i % 2) * 20
        lantern_color = "#FF4500" if not print_mode else "#E91E63"
        lantern_inner = "#FFA500" if not print_mode else "#FFEB3B"
        draw.ellipse([tx - 25, ty - 32, tx + 25, ty + 32], fill=lantern_color)
        draw.ellipse([tx - 18, ty - 28, tx + 18, ty + 28], fill=lantern_inner)
        draw.rectangle([tx - 15, ty - 37, tx + 15, ty - 31], fill="#111111")
        draw.rectangle([tx - 15, ty + 31, tx + 15, ty + 37], fill="#111111")
        if i < 19:
            next_tx = 75 + (i + 1) * 150
            next_ty = 220 + ((i + 1) % 2) * 20
            draw.line([(tx, ty), (next_tx, next_ty)], fill="#111111", width=3)
            
    # タイトルとサブタイトル
    title_color = "#FFD700" if not print_mode else "#111111"
    sub_color = "#FFFFFF" if not print_mode else "#555555"
    draw.text((width // 2, 90), f"大阪市盆踊りカレンダー 2026", fill=title_color, font=get_font(100, True), anchor="mm")
    draw.text((width // 2, 165), f"— {title_text} —", fill=sub_color, font=get_font(48, True), anchor="mm")
    
    # グリッド描画パラメータ
    x_offset = 100
    y_offset = 480
    cell_w = 400
    cell_h = 680
    
    # 曜日のヘッダー
    weeks = ["日曜日 (SUN)", "月曜日 (MON)", "火曜日 (TUE)", "水曜日 (WED)", "木曜日 (THU)", "金曜日 (FRI)", "土曜日 (SAT)"]
    for i, w in enumerate(weeks):
        color = "#FF4500" if i == 0 else ("#1E90FF" if i == 6 else ("#E0E0E0" if not print_mode else "#333333"))
        draw.text((x_offset + i * cell_w + cell_w//2, y_offset - 50), w, fill=color, font=get_font(30, True), anchor="mm")
        
    start_weekday = 2 if month == 7 else 5
    days_in_month = 31
    current_day = 1
    
    # カレンダーセルの描画
    for r in range(6):
        for c in range(7):
            cx = x_offset + c * cell_w
            cy = y_offset + r * cell_h
            
            # セル背景と枠線
            if print_mode:
                # 印刷用: すべてのマス目を市松模様なしで完全な純白背景に統一
                cell_bg_color = (255, 255, 255)
                draw.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=cell_bg_color, outline="#D1D1D6", width=2)
            else:
                # 通常用: 半透明グラスモルフィズム
                cell_bg = Image.new('RGBA', (cell_w, cell_h), (255, 255, 255, 12 if (c+r)%2==0 else 18))
                base.paste(cell_bg, (cx, cy), cell_bg)
                draw.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline="#ffffff33", width=2)
            
            if (r == 0 and c >= start_weekday) or (r > 0 and current_day <= days_in_month):
                # 日付
                date_color = "#FF4500" if c == 0 else ("#1E90FF" if c == 6 else ("#FFFFFF" if not print_mode else "#1C1C1E"))
                draw.text((cx + 25, cy + 25), str(current_day), fill=date_color, font=get_font(60, True))
                
                # イベントの描画
                if current_day in calendar_events[month]:
                    ev_list = calendar_events[month][current_day]
                    
                    # 件数バッジ
                    badge_bg = "#FF4500" if not print_mode else "#FF3B30"
                    draw.ellipse([cx + cell_w - 60, cy + 25, cx + cell_w - 20, cy + 65], fill=badge_bg)
                    draw.text((cx + cell_w - 40, cy + 45), str(len(ev_list)), fill="#FFFFFF", font=get_font(24, True), anchor="mm")
                    
                    # 予定リストの描画
                    for idx, ev in enumerate(ev_list):
                        ward_short = ev['ward'].replace('大阪市', '')
                        ev_text = f"• [{ward_short}]{ev['name']}"
                        
                        max_text_width = 350
                        current_font_size = 22
                        
                        # テキストがセル幅に収まるまでフォントサイズを動的に下げる
                        text_w = draw.textlength(ev_text, font=get_font(current_font_size, True))
                        while text_w > max_text_width and current_font_size > 12:
                            current_font_size -= 1
                            text_w = draw.textlength(ev_text, font=get_font(current_font_size, True))
                            
                        ex = cx + 25
                        ey = cy + 105 + idx * 42
                        
                        text_color = "#FFE4B5" if not print_mode else "#002D62"
                        draw.text((ex, ey), ev_text, fill=text_color, font=get_font(current_font_size, True))
                        
                current_day += 1
                
    # フッターの免責事項
    footer_text = "※免責事項: 本カレンダーは2026年7月1日時点の調査結果に基づくAIによる自動調査・生成物です。実際の開催情報と異なる場合があるため、お出かけの際は必ず各主催者の最新の公式発表をご確認ください。"
    footer_color = "#FF6347" if not print_mode else "#D32F2F"
    draw.text((width // 2, height - 80), footer_text, fill=footer_color, font=get_font(26, True), anchor="mm")
    
    # 保存
    base.save(output_filename)
    print(f"Saved ultra high-res calendar to {output_filename} (print_mode={print_mode})")

# 3. 実行
# 7月
generate_ultra_calendar(7, "7月 July 2026", '/Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_07.png', print_mode=False)
generate_ultra_calendar(7, "7月 July 2026 (印刷用)", '/Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_07_print.png', print_mode=True)

# 8月
generate_ultra_calendar(8, "8月 August 2026", '/Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_08.png', print_mode=False)
generate_ultra_calendar(8, "8月 August 2026 (印刷用)", '/Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_08_print.png', print_mode=True)

print("Finished all versions.")
