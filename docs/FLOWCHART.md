# 系統流程圖文件：隨便吃什麼都好系統 (Whatever Eatery)

根據產品需求文件 (PRD) 與技術架構 (ARCHITECTURE) 所設計的系統流程圖，包含使用者流程圖、系統序列圖與功能清單對照表。

## 1. 使用者流程圖（User Flow）

描述使用者進入系統後，操作各項核心功能（一鍵隨機推薦、多人決策輪盤、歷史紀錄）的路徑。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁]
    B --> C{選擇功能}
    
    %% 一鍵隨機推薦流程
    C -->|一鍵隨機推薦| D[設定極簡條件\n距離/價格/排除標籤]
    D --> E[點擊「隨便吃」按鈕]
    E --> F[顯示推薦結果與動畫]
    F --> G{滿意結果嗎？}
    G -->|是| H[一鍵導航至餐廳\n/ 加入我的最愛]
    G -->|否| I[點擊「換一個」\n短暫加入黑名單]
    I --> F
    
    %% 多人決策輪盤流程
    C -->|多人決策輪盤| J[建立輪盤房間]
    J --> K[分享連結/QR Code給好友]
    K --> L[眾人輸入提議選項]
    L --> M[啟動抽籤輪盤動畫]
    M --> N[顯示最終決定結果]
    N --> O[一鍵導航至餐廳]
    
    %% 歷史紀錄與收藏流程
    C -->|個人檔案與紀錄| P[查看個人歷史紀錄]
    P --> Q[檢視我的最愛清單]
    Q --> R[選擇最愛餐廳進行推薦]
```

## 2. 系統序列圖（Sequence Diagram）

描述「使用者點擊隨便吃（一鍵隨機推薦）」到「資料庫查詢並回傳結果」的完整系統資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask (後端 Route)
    participant DB as SQLite (資料庫)
    
    User->>Browser: 設定篩選條件並點擊「隨便吃」
    Browser->>Browser: 嘗試獲取地理位置 (Geolocation API)
    Browser->>Flask: POST /recommend (傳送條件與位置資料)
    
    Flask->>DB: 查詢符合條件且不在黑名單的餐廳
    DB-->>Flask: 回傳候選餐廳清單
    Flask->>Flask: 執行隨機演算法選出一家餐廳
    
    Flask-->>Browser: 回傳結果 (HTML/資料)
    Browser->>User: 播放盲盒動畫並顯示推薦結果
    
    opt 使用者點擊「導航」
        User->>Browser: 點擊「一鍵導航」
        Browser->>Browser: 開啟外部地圖服務 (Google/Apple Maps)
    end
    
    opt 使用者點擊「換一個」
        User->>Browser: 點擊「換一個」
        Browser->>Flask: POST /blacklist (傳送排除餐廳ID)
        Flask->>DB: 將該餐廳加入使用者暫時黑名單
        DB-->>Flask: 寫入成功
        Flask->>Flask: 從候選清單重新抽選
        Flask-->>Browser: 回傳新推薦結果
        Browser->>User: 顯示新結果
    end
```

## 3. 功能清單對照表

系統主要功能與對應的 URL 路徑、HTTP 方法之設計。

| 功能區塊 | 功能說明 | URL 路徑 | HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁** | 系統入口，提供隨機推薦表單與建立房間入口 | `/` | GET |
| **隨機推薦** | 接收條件與位置，回傳隨機抽選的餐廳結果 | `/recommend` | POST |
| **換一個 (黑名單)** | 將不滿意的結果加入短暫黑名單，並重抽餐廳 | `/blacklist` | POST |
| **我的最愛** | 將滿意的餐廳加入個人最愛清單 | `/favorite` | POST |
| **決策輪盤** | 建立一個新的多人決策輪盤房間 | `/room/create` | POST |
| **決策輪盤** | 進入特定的輪盤房間頁面 | `/room/<room_id>` | GET |
| **決策輪盤** | 在房間內提交想吃的選項 | `/room/<room_id>/propose` | POST |
| **決策輪盤** | 啟動房間的輪盤抽選並記錄結果 | `/room/<room_id>/spin` | POST |
| **個人檔案** | 查看個人的歷史推薦紀錄與最愛餐廳 | `/profile` | GET |
