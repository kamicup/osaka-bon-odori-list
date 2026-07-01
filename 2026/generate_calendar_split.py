import os
import re
from PIL import Image, ImageDraw, ImageFont

# 1. データの読み込みとパース
report_path = '/Users/yoshikazuhashimoto/tmp/bonodori_report_2026.md'
if not os.path.exists(report_path):
    report_path = '/Users/yoshikazuhashimoto/.gemini/antigravity-cli/brain/29c87b03-b41e-4f3a-9939-e5f07924f889/bonodori_report_2026.md'

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

# 2. カレンダー生成関数
def generate_monthly_calendar(month, title_text, output_filename):
    width = 3600
    height = 2400
    img = Image.new('RGB', (width, height), '#0A0E29')
    draw = ImageDraw.Draw(img)
    
    # グラデーション背景
    for y in range(height):
        r = int(0x0A + (0x1F - 0x0A) * (y / height))
        g = int(0x0E + (0x15 - 0x0E) * (y / height))
        b = int(0x29 + (0x3F - 0x29) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # タイトル
    draw.text((width // 2, 90), f"大阪市盆踊りカレンダー 2026 — {title_text}", fill="#FFD700", font=get_font(75, True), anchor="mm")
    
    # 提灯の装飾
    for i in range(30):
        tx = 60 + i * 122
        ty = 180 + (i % 2) * 15
        draw.ellipse([tx - 15, ty - 20, tx + 15, ty + 20], fill="#FFCC00")
        draw.rectangle([tx - 10, ty - 23, tx + 10, ty - 20], fill="#333333")
        draw.rectangle([tx - 10, ty + 20, tx + 10, ty + 23], fill="#333333")
        if i < 29:
            draw.line([(tx, ty), (tx + 122, ty + (1 - (i%2)*2)*15)], fill="#333333", width=2)
            
    # グリッド描画パラメータ
    x_offset = 120
    y_offset = 320
    cell_w = 480
    cell_h = 300
    
    # 曜日の描画
    weeks = ["日曜日 (SUN)", "月曜日 (MON)", "火曜日 (TUE)", "水曜日 (WED)", "木曜日 (THU)", "金曜日 (FRI)", "土曜日 (SAT)"]
    for i, w in enumerate(weeks):
        color = "#FF6347" if i == 0 else ("#1E90FF" if i == 6 else "#CCCCCC")
        draw.text((x_offset + i * cell_w + cell_w//2, y_offset - 40), w, fill=color, font=get_font(24, True), anchor="mm")
        
    start_weekday = 2 if month == 7 else 5 # 7/1は水曜、8/1は土曜
    days_in_month = 31
    current_day = 1
    
    # グリッドセルの描画
    for r in range(6):
        for c in range(7):
            cx = x_offset + c * cell_w
            cy = y_offset + r * cell_h
            
            # セル枠線の描画
            draw.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline="#ffffff44", width=2)
            
            if (r == 0 and c >= start_weekday) or (r > 0 and current_day <= days_in_month):
                # 日付（大きな数字）
                color = "#FF6347" if c == 0 else ("#1E90FF" if c == 6 else "#FFFFFF")
                draw.text((cx + 20, cy + 20), str(current_day), fill=color, font=get_font(48, True))
                
                # イベントの描画
                if current_day in calendar_events[month]:
                    ev_list = calendar_events[month][current_day]
                    
                    # 1日のイベント数バッジ
                    draw.ellipse([cx + cell_w - 45, cy + 20, cx + cell_w - 15, cy + 50], fill="#FF4500")
                    draw.text((cx + cell_w - 30, cy + 35), str(len(ev_list)), fill="#FFFFFF", font=get_font(18, True), anchor="mm")
                    
                    # 各予定を日付セル内に文字で描画
                    for idx, ev in enumerate(ev_list):
                        # 例: "[北区]うめだde盆踊り"
                        ward_short = ev['ward'].replace('大阪市', '')
                        ev_text = f"• [{ward_short}] {ev['name']}"
                        
                        # セルの横幅に合わせて適度にトリミング
                        if len(ev_text) > 18:
                            ev_text = ev_text[:17] + ".."
                            
                        # 件数に応じて1列または2列で描画
                        if len(ev_list) <= 6:
                            # 1列表示
                            ex = cx + 20
                            ey = cy + 90 + idx * 32
                            draw.text((ex, ey), ev_text, fill="#FFD700", font=get_font(18))
                        else:
                            # 2列表示 (左右に分割)
                            col = idx % 2
                            row = idx // 2
                            ex = cx + 15 + col * 235
                            ey = cy + 90 + row * 32
                            # 2列の場合はさらに短く
                            if len(ev_text) > 12:
                                ev_text = ev_text[:11] + ".."
                            draw.text((ex, ey), ev_text, fill="#FFD700", font=get_font(16))
                            
                current_day += 1
                
    # フッター特記事項
    footer_text = ""
    if month == 7:
        footer_text = "※注記: 7月22日・23日予定の今宮戎神社「こどもえびす」（浪速区）は本殿屋根葺替工事のため2026年夏は開催中止となります。"
    else:
        footer_text = "※注記: 8月16日・17日の「港区盆踊り大会」は出演者のブログ発表に基づく日程です。詳細な会場や時間は決定次第公開されます。"
    draw.text((width // 2, height - 60), footer_text, fill="#FF6347", font=get_font(24, True), anchor="mm")
    
    # 保存
    img.save(output_filename)
    print(f"Saved monthly calendar to {output_filename}")

# 3. カレンダーの生成
generate_monthly_calendar(7, "7月 July 2026", '/Users/yoshikazuhashimoto/tmp/大阪市盆踊りカレンダー2026_07.png')
generate_monthly_calendar(8, "8月 August 2026", '/Users/yoshikazuhashimoto/tmp/大阪市盆踊りカレンダー2026_08.png')
print("All tasks completed.")
