import os
import re
import datetime
from PIL import Image, ImageDraw, ImageFont

# 1. データの読み込みとパース
report_path = '/Users/yoshikazuhashimoto/tmp/bonodori_report_2026.md'
if not os.path.exists(report_path):
    # アーティファクトからコピー
    report_path = '/Users/yoshikazuhashimoto/.gemini/antigravity-cli/brain/29c87b03-b41e-4f3a-9939-e5f07924f889/bonodori_report_2026.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

def parse_date(date_str):
    # 例: "2026年7月10日（金）<br>～7月11日（土）"
    # 例: "2026年7月25日（土）"
    months_days = []
    # 年を除去
    date_str = re.sub(r'^\d+年', '', date_str)
    # 月と日を抽出
    matches = re.findall(r'(\d+)月\s*(\d+)日', date_str)
    for m, d in matches:
        months_days.append((int(m), int(d)))
    
    # 連続日程の補完 (例: 7月31日～8月1日 のような場合で中間の日付があるか)
    # 基本的にこのデータセットでは2日間開催が多く、matchesで両日とも抽出されるため補完不要。
    return months_days

events = []
# テーブル部分の抽出
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
                    'date_str': date_str.replace('<br>', ' '),
                    'name': name,
                    'place': place,
                    'ward': ward,
                    'notes': notes
                })

# 日付ごとのマップを作成
calendar_events = {7: {}, 8: {}}
for ev in events:
    for m, d in ev['dates']:
        if m in [7, 8]:
            if d not in calendar_events[m]:
                calendar_events[m][d] = []
            calendar_events[m][d].append(ev)

# 2. 画像描画の準備
width = 3000
height = 2200
img = Image.new('RGB', (width, height), '#0A0E29')
draw = ImageDraw.Draw(img)

# グラデーション背景の描画
for y in range(height):
    # 深紺 #0A0E29 から 暗紫 #1E1233 へのグラデーション
    r = int(0x0A + (0x1E - 0x0A) * (y / height))
    g = int(0x0E + (0x12 - 0x0E) * (y / height))
    b = int(0x29 + (0x33 - 0x29) * (y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# フォントの選択
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
        # TTCファイルの場合はインデックスを指定する
        return ImageFont.truetype(font_path, size, index=1 if bold else 0)
    else:
        return ImageFont.load_default()

# 3. タイトル等の描画
draw.text((width // 2, 80), "大阪市盆踊りカレンダー 2026", fill="#FFD700", font=get_font(75, True), anchor="mm")
draw.text((width // 2, 145), "〜 信頼できる公式情報源に基づく全件掲載版 〜", fill="#FFFFFF", font=get_font(30), anchor="mm")

# 4. カレンダーの描画関数
def draw_calendar(x_offset, y_offset, month, title):
    draw.text((x_offset + 350, y_offset - 40), title, fill="#FFFFFF", font=get_font(45, True), anchor="mm")
    
    # 曜日の描画
    weeks = ["日", "月", "火", "水", "木", "金", "土"]
    cell_w = 100
    cell_h = 75
    
    for i, w in enumerate(weeks):
        color = "#FF6347" if i == 0 else ("#1E90FF" if i == 6 else "#CCCCCC")
        draw.text((x_offset + i * cell_w + cell_w//2, y_offset + 20), w, fill=color, font=get_font(22, True), anchor="mm")
    
    # 日付グリッドの計算
    # 2026年7月1日は水曜日 (weekday=2)
    # 2026年8月1日は土曜日 (weekday=5)
    start_weekday = 2 if month == 7 else 5
    days_in_month = 31
    
    current_day = 1
    row = 0
    
    # グリッド枠の描画
    for r in range(6):
        for c in range(7):
            cx = x_offset + c * cell_w
            cy = y_offset + 50 + r * cell_h
            # 薄い白の枠線
            draw.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline="#ffffff33", width=1)
            
            # 日付のプロット
            if (r == 0 and c >= start_weekday) or (r > 0 and current_day <= days_in_month):
                # 日曜日か土曜日かで色を変える
                color = "#FF6347" if c == 0 else ("#1E90FF" if c == 6 else "#FFFFFF")
                draw.text((cx + 10, cy + 10), str(current_day), fill=color, font=get_font(20, True))
                
                # イベントの有無をチェック
                if current_day in calendar_events[month]:
                    ev_list = calendar_events[month][current_day]
                    num_events = len(ev_list)
                    
                    # 赤い提灯マーク（円）を描画
                    draw.ellipse([cx + cell_w - 35, cy + 10, cx + cell_w - 10, cy + 35], fill="#FF4500")
                    draw.text((cx + cell_w - 225/10, cy + 225/10), str(num_events), fill="#FFFFFF", font=get_font(14, True), anchor="mm")
                    
                    # 最初のイベントの区を小さく表示
                    wards = list(set([e['ward'] for e in ev_list]))
                    ward_text = ",".join([w.replace('区', '') for w in wards[:2]])
                    if len(wards) > 2:
                        ward_text += ".."
                    draw.text((cx + cell_w//2, cy + cell_h - 20), ward_text, fill="#FFD700", font=get_font(14), anchor="mm")
                
                current_day += 1

# カレンダーの配置
draw_calendar(150, 250, 7, "7月 July")
draw_calendar(1650, 250, 8, "8月 August")

# 提灯装飾を上部に描画
for i in range(25):
    tx = 60 + i * 120
    ty = 180 + (i % 2) * 15
    # 黄色の円
    draw.ellipse([tx - 15, ty - 20, tx + 15, ty + 20], fill="#FFCC00")
    # 提灯の上下の黒いパーツ
    draw.rectangle([tx - 10, ty - 23, tx + 10, ty - 20], fill="#333333")
    draw.rectangle([tx - 10, ty + 20, tx + 10, ty + 23], fill="#333333")
    # つなぎの黒い線
    if i < 24:
        draw.line([(tx, ty), (tx + 120, ty + (1 - (i%2)*2)*15)], fill="#333333", width=2)

# 5. リストの描画
# 7月イベントリストの描画 (左側下部)
draw.text((150, 780), "【 7月の盆踊り開催日程一覧 】", fill="#FFD700", font=get_font(32, True))
y_cursor = 840

# 7月のイベントを日付順に並べ替え
july_events = []
for day in sorted(calendar_events[7].keys()):
    for ev in calendar_events[7][day]:
        if ev not in july_events:
            july_events.append(ev)

for ev in july_events:
    # 表示用のテキスト
    date_label = ev['date_str'].replace('2026年', '').strip()
    text = f"● {date_label}  【{ev['ward']}】  {ev['name']}\n   場所：{ev['place']}"
    
    # 描画
    draw.text((150, y_cursor), text, fill="#FFFFFF", font=get_font(22))
    y_cursor += 75

# 8月イベントリストの描画 (下部全体または2列レイアウト)
draw.text((150, 1300), "【 8月の盆踊り開催日程一覧 】", fill="#FFD700", font=get_font(32, True))

# 8月のイベントを抽出
aug_events = []
for day in sorted(calendar_events[8].keys()):
    for ev in calendar_events[8][day]:
        if ev not in aug_events:
            aug_events.append(ev)

# 8月は件数が多いため2列に分割して配置する
col1_x = 150
col2_x = 1550
y_start = 1360
y_cursor_l = y_start
y_cursor_r = y_start

mid_point = len(aug_events) // 2 + 1

for idx, ev in enumerate(aug_events):
    date_label = ev['date_str'].replace('2026年', '').strip()
    text = f"● {date_label}  【{ev['ward']}】  {ev['name']}\n   場所：{ev['place']}"
    
    if idx < mid_point:
        draw.text((col1_x, y_cursor_l), text, fill="#FFFFFF", font=get_font(20))
        y_cursor_l += 65
    else:
        draw.text((col2_x, y_cursor_r), text, fill="#FFFFFF", font=get_font(20))
        y_cursor_r += 65

# フッターの特記事項
draw.text((width // 2, height - 60), 
          "※今宮戎神社「こどもえびす」（浪速区）は本殿屋根葺替工事のため2026年夏は開催中止となります。", 
          fill="#FF6347", font=get_font(22, True), anchor="mm")

# 画像の保存
output_path = '/Users/yoshikazuhashimoto/tmp/大阪市盆踊りカレンダー2026.png'
img.save(output_path)
print(f"Calendar saved successfully to {output_path}")
