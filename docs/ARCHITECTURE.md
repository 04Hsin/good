# 系統架構設計：隨便吃什麼都好系統 (Whatever Eatery)

根據產品需求文件 (PRD) 與技術限制，本專案將採用輕量級的後端框架與模板渲染引擎來實現，以達到快速開發與容易維護的目標。

## 1. 技術架構說明

本系統採用經典的 **MVC (Model-View-Controller)** 架構模式，技術選型如下：

* **後端框架 (Controller)**：`Python + Flask`
  * **選用原因**：Flask 是輕量級的 Python 框架，適合快速建立功能聚焦的 Web 應用（如隨機推薦系統與抽籤輪盤）。其靈活性高，不需像大型框架那樣帶入過多不需要的功能。
  * **職責**：處理使用者請求（例如點擊「隨便吃」按鈕、建立多人房間）、業務邏輯處理（隨機演算法、篩選邏輯）、與資料庫進行互動。
* **模板引擎 (View)**：`Jinja2`
  * **選用原因**：與 Flask 原生整合，不需前後端分離，直接由後端渲染 HTML 頁面後回傳給瀏覽器，降低部署與架構複雜度。配合原生 JavaScript 和 CSS 即可實現各種互動效果（如盲盒動畫、決策輪盤）。
  * **職責**：將 Controller 傳遞的資料結合 HTML 模板，呈現終端使用者介面。
* **資料庫 (Model)**：`SQLite` (搭配 SQLAlchemy 或 sqlite3)
  * **選用原因**：無需額外設定伺服器即可運作，資料儲存在單一檔案中，適合此系統的輕量級資料儲存需求（如餐廳清單、使用者收藏、歷史紀錄）。
  * **職責**：定義資料結構（餐廳資料表、使用者偏好、房間資料），負責資料的持久化儲存與查詢。

## 2. 專案資料夾結構

建議的資料夾結構如下，以模組化的方式組織程式碼，方便後續維護與擴充：

```text
whatever-eatery/
├── app/                        # Flask 應用程式主要資料夾
│   ├── __init__.py             # 初始化 Flask 應用程式與資料庫
│   ├── models/                 # 資料庫模型 (Model)
│   │   └── database.py         # 定義 User, Restaurant, Room 等資料表結構
│   ├── routes/                 # 路由與 Controller 邏輯
│   │   ├── main.py             # 處理首頁、一鍵隨機推薦等核心路由
│   │   ├── roulette.py         # 處理多人決策輪盤相關邏輯
│   │   └── user.py             # 處理歷史紀錄、收藏、偏好設定等
│   ├── templates/              # Jinja2 HTML 模板 (View)
│   │   ├── base.html           # 全域共用的基礎模板 (Navbar, Footer)
│   │   ├── index.html          # 首頁 (一鍵推薦與篩選介面)
│   │   ├── roulette.html       # 多人輪盤抽籤介面
│   │   └── profile.html        # 個人歷史紀錄與收藏介面
│   └── static/                 # 靜態資源 (CSS, JS, 圖片)
│       ├── css/
│       │   └── style.css       # 全域樣式，包含極簡風格與響應式設計
│       ├── js/
│       │   ├── main.js         # 前端共用邏輯 (定位授權、導航跳轉)
│       │   └── animations.js   # 盲盒與輪盤等趣味動畫邏輯
│       └── images/             # 系統圖片與 icon
├── instance/                   # 存放本機特定檔案
│   └── database.db             # SQLite 資料庫檔案
├── docs/                       # 專案文件
│   ├── PRD.md                  # 產品需求文件
│   └── ARCHITECTURE.md         # 系統架構文件 (本文件)
├── requirements.txt            # Python 依賴套件清單 (Flask, SQLAlchemy 等)
└── app.py                      # 系統執行入口檔案
```

## 3. 元件關係圖

以下是系統核心運作的元件關係圖，展示瀏覽器、Flask Controller、Model 與資料庫之間的資料流：

```mermaid
flowchart TD
    Browser[瀏覽器 (Client)] -->|HTTP Request\n(如：點擊隨便吃)| Routes[Flask Routes\n(Controller)]
    
    subgraph 伺服器端 (Server)
        Routes <-->|查詢/寫入資料| Models[Models\n(SQLAlchemy/sqlite3)]
        Routes -->|傳遞資料與狀態| Templates[Jinja2 Templates\n(View)]
    end
    
    Models <-->|讀寫| DB[(SQLite\nDatabase)]
    Templates -->|HTML 渲染| Routes
    
    Routes -->|HTTP Response\n(HTML/CSS/JS)| Browser
```

## 4. 關鍵設計決策

1. **採用不分離架構 (Server-Side Rendering)**：
   * **原因**：為了在短時間內完成開發並維持系統簡單，我們不使用 React/Vue 等前端框架，而是透過 Flask + Jinja2 直接輸出 HTML。這樣可以大幅降低前後端 API 串接的複雜度，並且符合技術限制要求。針對如輪盤等動態互動，則依賴原生的 JavaScript 來處理前端動畫。
2. **行動優先 (Mobile-First) 設計**：
   * **原因**：使用者通常是在路上或餐廳外使用手機來決定「吃什麼」。因此前端頁面的 CSS 設計將以行動裝置的單手操作為核心考量，按鈕需夠大，佈局需極簡，避免複雜的表單填寫。
3. **無摩擦體驗 (Frictionless UX) 的資料庫設計**：
   * **原因**：考量到目標用戶希望「決策成本」降至最低，系統應允許未註冊使用者即可體驗「一鍵隨機推薦」功能（Guest Mode）。因此在 Model 設計上，使用者的偏好（如「黑名單」）可先暫存在前端的 `localStorage` 或 Session 中，直到使用者願意登入才將資料持久化存入 SQLite，降低使用門檻。
4. **地理位置處理策略**：
   * **原因**：推薦依賴於使用者的「當下位置」。系統將在前端透過 JavaScript 的 Geolocation API 獲取經緯度，並在點擊推薦時一併傳送給 Flask 後端。若使用者拒絕授權定位，則退回「手動輸入大致區域」的替代方案，確保系統可用性。
