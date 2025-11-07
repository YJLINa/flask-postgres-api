# Flask PostgreSQL API for Copilot

這是一個簡單的 Flask API，可連線 PostgreSQL 資料庫並回傳查詢結果。
可直接部署於 [Render.com](https://render.com)。

## 部署步驟

1. Fork 這個專案到你自己的 GitHub。
2. 登入 Render → 建立新的 Web Service。
3. 選擇這個專案。
4. 設定：
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3.10+
5. 新增環境變數：
6. 部署完成後，Render 會提供一個 HTTPS URL，例如：
7. 將這個 URL 填入 Copilot Studio 的 Custom Connector 即可。
