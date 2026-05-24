import subprocess
import datetime
import os

def auto_git_push():
    print("开始自动推送更新到 GitHub...")
    try:
        # 1. 暂存所有更改 (等同于 git add .)
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. 生成带有当天日期的提交信息
        commit_message = f"Auto-update: 竞品情报更新 {datetime.date.today()}"
        
        # 3. 提交更改 (等同于 git commit -m "...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # 4. 推送到远端仓库 (等同于 git push)
        subprocess.run(["git", "push"], check=True)
        
        print("✅ 成功推送到 GitHub！Vercel 将在几分钟内自动完成网站更新。")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 推送过程遇到问题（可能是没有新的数据更改）: {e}")

if __name__ == "__main__":
    auto_git_push()