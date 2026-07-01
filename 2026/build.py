import os
import sys
import subprocess

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"Error: {script_name} not found at {script_path}")
        return False
    
    print(f"Running {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}:")
        print(e.stderr)
        return False

def main():
    print(f"Using Python: {sys.executable}")

    print("==================================================")
    print("大阪市盆踊りプロジェクト 一括ビルドシステム")
    print("==================================================")
    
    # HTMLカレンダー & JSONデータソースの生成
    if not run_script("generate_calendar_html.py"):
        print("Build failed at HTML/JSON generation step.")
        sys.exit(1)
        
    print("==================================================")
    print("🎉 ビルドが正常に完了しました！")
    print("以下の成果物がすべて更新されました：")
    print(" - docs/index.html (HTMLビュー)")
    print(" - docs/events.json (JSONデータソース)")
    print("==================================================")
    print("Gitへのコミット・プッシュを実行する準備が整いました。")

if __name__ == "__main__":
    main()
