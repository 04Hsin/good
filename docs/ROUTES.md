# API 路由與頁面設計：隨便吃什麼都好系統 (Whatever Eatery)

根據 PRD、系統架構與資料庫設計，規劃本系統的 Flask 路由 (Routes)、HTTP 方法及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能區塊 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與推薦** | GET | `/` | `templates/index.html` | 系統入口，顯示篩選表單、推薦結果與建立房間入口。 |
| **首頁與推薦** | POST | `/recommend` | `templates/index.html` | 接收篩選條件與定位，查詢資料庫並回傳隨機推薦的餐廳，顯示盲盒動畫。 |
| **互動操作** | POST | `/blacklist` | — (重導向 `/`) | 將不滿意的餐廳短暫加入黑名單，並自動重新觸發推薦。 |
| **互動操作** | POST | `/favorite` | — (重導向 `/profile`) | 將滿意的餐廳加入個人的最愛清單。 |
| **決策輪盤** | POST | `/room/create` | — (重導向房間) | 建立新的多人決策輪盤房間，產生 UUID。 |
| **決策輪盤** | GET | `/room/<room_id>` | `templates/roulette.html` | 顯示特定房間頁面，包含現有提議與抽籤輪盤介面。 |
| **決策輪盤** | POST | `/room/<room_id>/propose` | — (重導向房間) | 參與者在房間內提交想吃的選項，寫入資料庫。 |
| **決策輪盤** | POST | `/room/<room_id>/spin` | — (回傳 JSON) | 啟動輪盤抽選，系統隨機選出結果並更新房間狀態。 |
| **使用者管理** | GET/POST | `/login` | `templates/login.html` | 會員登入。 |
| **使用者管理** | GET/POST | `/register` | `templates/register.html` | 會員註冊。 |
| **使用者管理** | GET | `/logout` | — (重導向 `/`) | 會員登出。 |
| **使用者管理** | GET | `/profile` | `templates/profile.html` | 查看使用者的歷史推薦紀錄與我的最愛清單。 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁與推薦 (`app/routes/main.py`)

#### `GET /` (首頁)
- **輸入**：無
- **處理邏輯**：判斷使用者是否登入，準備極簡條件篩選表單。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：無。

#### `POST /recommend` (一鍵隨機推薦)
- **輸入**：表單資料（距離範圍、價格區間、排除條件標籤），地理位置（經緯度）。
- **處理邏輯**：
  1. 根據條件過濾 `RESTAURANT` 表。
  2. 排除 `BLACKLIST` 中尚未過期的餐廳。
  3. 隨機抽選一家餐廳，若使用者已登入，寫入 `SEARCH_HISTORY`。
- **輸出**：渲染 `index.html`，並將推薦結果傳遞給模板以觸發動畫。
- **錯誤處理**：若無符合條件的餐廳，回傳提示訊息請使用者放寬篩選條件。

---

### 2.2 互動操作與使用者管理 (`app/routes/user.py`)

#### `POST /blacklist` (加入黑名單並重抽)
- **輸入**：`restaurant_id`
- **處理邏輯**：將該餐廳加入 `BLACKLIST`，設為暫時排除（例如 7 天），隨後再次觸發隨機推薦邏輯。
- **輸出**：重導向至 `/` 並帶有新的推薦結果。

#### `POST /favorite` (加入我的最愛)
- **輸入**：`restaurant_id`
- **處理邏輯**：檢查是否登入，若未登入引導至登入頁。若已登入則寫入 `FAVORITE` 表。
- **輸出**：重導向至來源頁面或 `/profile`，帶有成功訊息。

#### `GET /profile` (個人檔案)
- **輸入**：無（依賴 Session / 登入狀態）
- **處理邏輯**：驗證登入。從 `SEARCH_HISTORY` 獲取近期紀錄，從 `FAVORITE` 獲取最愛清單。
- **輸出**：渲染 `profile.html`。

*(`/login`, `/register`, `/logout` 為標準的認證邏輯，在此不贅述)*

---

### 2.3 多人決策輪盤 (`app/routes/roulette.py`)

#### `POST /room/create` (建立房間)
- **輸入**：建立者 ID (若有登入)
- **處理邏輯**：產生一組唯一的 UUID 作為房間 ID，新增一筆紀錄到 `ROOM` 表。
- **輸出**：重導向至 `/room/<room_id>`。

#### `GET /room/<room_id>` (進入房間)
- **輸入**：URL 參數 `room_id`
- **處理邏輯**：查詢 `ROOM` 是否存在且狀態是否開啟。讀取該房間的 `PROPOSAL` 列表。
- **輸出**：渲染 `roulette.html`。
- **錯誤處理**：若房間不存在，顯示 404 或重導向回首頁。

#### `POST /room/<room_id>/propose` (提交提議)
- **輸入**：表單資料 `user_name`、`restaurant_name` 或選擇的 `restaurant_id`
- **處理邏輯**：驗證房間狀態為開放中，新增選項到 `PROPOSAL` 表。
- **輸出**：重導向回 `/room/<room_id>` 更新畫面。

#### `POST /room/<room_id>/spin` (啟動輪盤)
- **輸入**：URL 參數 `room_id`
- **處理邏輯**：
  1. 僅限房間建立者或第一位加入者觸發。
  2. 從該房間的所有 `PROPOSAL` 中隨機抽選一項。
  3. 更新 `ROOM` 狀態為已關閉 (`closed`)，並記錄最終 `result_id`。
- **輸出**：回傳 JSON 資料包含抽中結果，供前端 JavaScript 播放輪盤動畫。

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 資料夾，並採用繼承架構：

1. **`base.html`**
   - **說明**：全域基礎模板，包含 HTML 結構、Navbar（導覽列：回首頁、登入、個人檔案）、Footer，並引入全域 CSS/JS。所有其他模板皆繼承此檔案。
2. **`index.html`**
   - **繼承**：`base.html`
   - **說明**：首頁。包含極簡的推薦篩選表單、「隨便吃」按鈕、以及盲盒動畫顯示區塊與推薦結果展示。
3. **`roulette.html`**
   - **繼承**：`base.html`
   - **說明**：決策房間頁面。顯示房間連結 (QR Code)、已提交的提議列表、新增提議的表單、以及視覺化的大型抽籤輪盤。
4. **`profile.html`**
   - **繼承**：`base.html`
   - **說明**：個人資料頁面。顯示「歷史紀錄」與「我的最愛」兩個區塊。
5. **`login.html`** & **`register.html`**
   - **繼承**：`base.html`
   - **說明**：基本的會員登入與註冊表單。

---

## 4. 路由骨架程式碼規劃

請參閱 `app/routes/` 下的對應 Python 檔案：
- `app/routes/__init__.py`
- `app/routes/main.py`
- `app/routes/user.py`
- `app/routes/roulette.py`
