# Max 蛋黃酥上車機器人

## 總覽

MaxBot 是一個開放原始碼的蛋黃酥/公車訂位機器人。祝您搶購成功。

搶票機制，就是在比誰的比較快送出訂單，機器人一定比純手工點擊的快。

售票系統的「驗證碼」機制會讓一般不會寫程式的民眾更難公平地購買到預期的門票，因為機器人可以自動填入驗證碼內容。

部份的售票系統可以透過「人海戰術」來提升買到票的機率，因此建議大家可以麻煩親朋好友去註冊售票系統的帳號。注意：在使用他人的帳號搶票之前，一定要告知當事人用途，並徵詢同意與授權。

MaxBot 的出發點是讓一般民眾與代購黃牛或懂得寫程式的人有類似的基準點或類似的起跑線上，用魔法對抗魔法，當某一天大家都是透過機器人來搶票時，當機器人數量已多到影響一般民眾購票的權利時，售票業者才比較有可能會對未來熱門演唱會改採「實名制」+「抽籤制」，讓更多民眾可以公平地購買到門票，就可以跟「人海戰術」與「搶票機器人」說 bye-bye 。

台灣藝文活動的文創法第十條中的「不正方式」由於沒有明確定義，代表的是所有軟體都涉嫌違反。故在此呼籲大家，勿以身試法。

以下文章出現的「搶票」指的是「非台灣的藝文活動或車票」。

MaxBot is a FREE and open source bot program. Good luck getting your expected food or bus seat.

## LEGAL NOTICE 法律聲明

<details>
<summary><code><b>法律聲明</b>（點我展開）</code></summary>

作者沒有意圖要他人購得的票券進行加價轉售或是使用在違法的事情上，他人的行為並不在作者的意識支配範圍之內，作者不對他人的非法行為負責。

使用此儲存庫或與之相關的任何程式碼，即表示您同意[法律聲明](https://github.com/max32002/tixcraft_bot/blob/master/LEGAL_NOTICE.md)。作者不對該儲存庫的使用負責與背書，也不對其他使用者所做的任何副本、分叉、重新上傳或與 MaxBot 相關的任何其他內容負責。 這是作者唯一的帳戶和儲存庫。 為了防止假冒或不負責任的行為，請遵守此儲存庫使用的 GNU GPL 授權。

</details>

## Protect Account 保護你的帳戶

<details>
<summary><code><b>保護你的帳戶</b>（點我展開）</code></summary>

目前的售票系統售票無法阻擋機器人進行購票，官方只能從伺服器存取記錄來看到速度過快的記錄，並將之視之為機器人，對其封鎖帳號，短時間刷新幾秒會被鎖帳號並沒有明確的遊戲規則。

Q：在沒有違法的前提下，要搶拓元的蛋黃酥與 KKTIX 的（非台灣）海外活動，怎麼才不會被官方鎖帳號？

A：從之前 MaxBot 執行秒數來看，較好的電腦花費秒數大約 8 秒，一般電腦大約花費 10 ～ 12 秒，以秒殺的蛋黃酥來說，建議設定機器人啟動時間為開搶前 2 秒，停止時間為開搶後的 15 秒，是可以降低被官方鎖帳號的機率。

而清票，需要長時間地重新整理，請以自然人能處理的前提下，設定重新整理的延遲時間為一般人可以處理的 2 秒以上。

如果說你想增加在伺服器上存取記錄的變化程度，可以使用秒數的關鍵字功能，讓 MaxBot 在特定秒數時啟動與暫停。參考影片：https://youtu.be/u3YQCZZu6kE

MaxBot 的出發點是幫助大家在購票時，可以有效率地自動化在花時間、重覆又無聊的刷新網頁。如果有任何違法，必定立即修正。

</details>

## Download 蛋黃酥上車程式下載

<details>
<summary><code><b>蛋黃酥上車程式下載</b>（點我展開）</code></summary>

https://github.com/max32002/tixcraft_bot/releases

下載說明:

- 目前有打包的「執行檔」，只有 Windows 平台，其他作業系統需要使用原始碼來執行。當然 Windows 平台也可以用原始碼執行 MaxBot.
- 如果你是要用「原始碼」執行 MaxBot, 在透過 git clone 或在 github 按下載原始碼的 zip 檔，你的 python 版本可以使用 3.7 / 3.8 / 3.9 / 3.10 這 4 個版號。
- 如果有辦法的話，建議使用原始碼來執行 MaxBot，執行上的「效率」與「相容性」的問題會較少。

</details>

## Demo 示範影片

[點此查看示範影片](https://github.com/max32002/tixcraft_bot/blob/master/demo_video.md)

## How to Use 如何使用

<details>
<summary><code><b>如何使用</b>（點我展開）</code></summary>

- tixcraft / indievox / ticketmaster: https://max-everyday.com/2018/03/tixcraft-bot/
- kktix: https://max-everyday.com/2018/12/kktix-bot/
- cityline: https://max-everyday.com/2019/03/cityline-bot/
- urbtix: https://max-everyday.com/2019/02/urbtix-bot/
- hkticketing / galaxymacau: https://max-everyday.com/2023/01/hkticketing-bot/

</details>

## How to Execute Source Code 透過原始碼的執行方法

<details>
<summary><code><b>透過原始碼的執行方法</b>（點我展開）</code></summary>

透過原始碼執行 MaxBot 教學影片：
https://youtu.be/HpVG91j0lbI

使用原始碼的解法，第一步是先取得原始碼後，開啟 Terminal(終端機) 視窗來下指令，應該是 4 行指令就可以了。

請參看看文章: 如何用虛擬主機搶拓元的門票，這篇文章是以虛擬主機來示範，在 Windows / macOS / Linux 平台裡的 python 操作方式幾乎相同。

詳細的文字說明:
https://max-everyday.com/2023/11/buy-ticket-by-vm/

### Step 1: 取得 source code:

```bash
git clone https://github.com/max32002/tixcraft_bot.git
```

### Step 2: 進入 clone 的資料夾: tixcraft_bot:

```bash
cd tixcraft_bot
```

### Step 3: 安裝第三方套件:

```bash
python3 -m pip install -r requirement.txt
```

### Step 4: 執行設定介面主桯式:

```bash
python3 settings.py
```

- 如果不使用設定介面，直接執行主程式:

```bash
python3 chrome_tixcraft.py
```

- 如果不使用設定介面，直接執行主程式並套用特定的設定檔:

```bash
python3 chrome_tixcraft.py --input settings.json
```

#### 如果遇到 MaxBot 改版, 請重新操作上面 4 個步驟一次, 即可取得新的版本.

#### 如果 MaxBot 沒改版, 第二次要再執行的話, 使用 Step 2 + Step 4, 這 2 行指令, 就可以執行 MaxBot.

#### 如果你是 ARM CPU 應該會在 Step 3 就顯示錯誤訊息, 解法:

https://github.com/max32002/tixcraft_bot/issues/82#issuecomment-1878986084

不管是 macOS 還是 Windows 預設都是沒有 git 這個指令，如果 Step 1 執行後, 沒有檔案被下載, 請先安裝 git 到你的作業系統。或是使用 github 網頁裡的 Download 功能把 python 腳本下載。

如果你選擇下載 github 上的 zip 檔, 在 Step 2 進入目錄的指令可能會遇到問題, 因為「直接解壓縮」後的目錄名稱並不是 tixcraft_bot 而是 tixcraft_bot-master, 你在進入的資料夾名稱, 需要調整為你實際解壓縮後的目錄名稱。

透過瀏覽器下載 github 上的 zip 檔, 在 Windows / macOS / Linux 平台, 預設的路徑在「下載」(~/Download) 的資料夾, 你在執行的 Terminal 視窗的路徑, 與你解壓縮的路徑可能不同, 直接執行上面的指令, 會無法進入到預期的資料夾內。

### Q: 取得 source code 後跑出來 fatal: destination path 'tixcraft_bot' already exists and is not an empty directory.想問是什麼意思?

<b>A: </b>執行 git clone 2 次, 重覆取得 source code, 才會有這個問題, 如果 tixcraft_bot 目錄已經存在, 直接
<code>cd tixcraft_bot</code>
就可以了。
如果你想把已下載的刪除, 可以直接把 tixcraft_bot 目錄刪掉即可。
如果你想更新 source code, 可以重新下載, 或是先 <code>cd tixcraft_bot</code> 目錄後, 再執行<code>git pull</code>, 可以更新 source code 為新的版本。

#### PS:

- 請先確定你的 python 執行環境下已安裝 selenium 或 nodriver 及相關的套件，請參考 requirement.txt 檔案內容。
- 透過 python3 執行 settings.py 就可以有 GUI 的設定介面。
- 如果你是使用 macOS 並且執行環境沒有 python3，請 python 官方網站([https://www.python.org/downloads/](https://www.python.org/downloads/))來安裝 python3.
- 如果你是使用 Firefox, ChromeDriver 的元件是叫 geckodriver，下載點在：https://github.com/mozilla/geckodriver/releases ，與 ChromeDriver 的處理方式是一樣，如果是 mac 電腦，要在元件按右鍵開啟，做一次授權的動作，mac 有 2 個版本，-macos.tar.gz 與 -macos-aarch64.tar.gz ，如果是 intel CPU 的版本，請服用前面沒有 aarch64 的版本。

#### PS：

搶票程式可以多開 chrome 瀏覽器，如果你電腦效能高。但如果開太多瀏覽器會顯示 Out of Memory, 請增加 Windows 的虛擬記憶體:
https://zh-tw.emeditor.com/increase-virtual-memory/

#### PS：

「掛機模式」的選項，指人不需要在電腦前，驗證碼會猜到對為止。

### Q: 是只有使用虛擬主機才要用程式碼執行搶票機器人嗎？

**A:** 除了 Window 有打包的執行檔之外, macOS / Linux 只能使用原始碼來執行, 當然 Windows 也可以用原始碼來執行.

</details>

## File Description 檔案說明

<details>
<summary><code><b>檔案說明</b>（點我展開）</code></summary>

- chrome_tixcraft.py : 搶票機器人主程式，用來自動化網頁的操作，使用元件是 selenium。
- nodriver_tixcraft.py : 也是搶票機器人主程式，用來自動化網頁的操作，使用的元件是 nodriver。
- settings.py : 編輯 settings.json 的 GUI 介面。提供圖片 OCR 功能給 chrome 擴充功能。支援定時啟用/停用 MaxBot。
- settings_old.py : 舊版本的編輯 settings.json 的 GUI 介面，與 settings.py 的差別在介面一個是網頁形式，old 的用的是視窗形式。
- config_launcher.py : 設定檔管理, 方便對多個設定檔案搶票。
</details>

## Introduce the Implement 實作方法

[實作方法 點我查看](https://stackoverflow.max-everyday.com/2018/03/selenium-chrome-webdriver/)

## Execute Suggestion 蛋黃酥上車相關建議

<details>
<summary><code><b>蛋黃酥上車相關建議</b>（點我展開）</code></summary>

please run this source code with high performance hardware computer and high speed + stable network.

門票的「限量」是很殘酷的，建議不要用破舊的電腦或連線不穩的手機網路來搶票，因為只要比別人慢個 0.1 秒，票可能就沒了。為了要搶到限量的票真心建議去一下網咖或找一個網路連線穩定且快的地方並使用硬體不差的電腦來搶票。

</details>

## TODO about Cpatcha 關於驗證碼

<details>
<summary><code><b>關於驗證碼</b>（點我展開）</code></summary>

目前自動輸入驗證碼用的元件是:

https://github.com/sml2h3/ddddocr

附註：

- 由於 ddddocr 元件的因素，python 版本要降到 3.10.11 版, 傳送門:
  https://www.python.org/downloads/release/python-31011/
- 猜測驗證碼時比較容易出錯的是字英 f 和 t，還有 q 和 g, v 和 u 還有 w.

想自動輸入驗證碼，除了可以使用 ddddocr 提供的 trainer, 也可以參考看看：實作基於 CNN 的台鐵訂票驗證碼辨識以及透過模仿及資料增強的訓練集產生器 (Simple captcha solver based on CNN and a training set generator by imitating the style of captcha and data augmentation)

https://github.com/JasonLiTW/simple-railway-captcha-solver

</details>

## Common Problems 常見問題整理

<details>
<summary><code><b>常見問題整理</b>（點我展開）</code></summary>

### 整理大家在搶票時常遇到的問題：

- [使用搶票程式有違法嗎？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#law)
- [沒講清楚成功後的報酬](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#reward)
- [買到太多票](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#too_many_ticket)
- [如何處理多的票？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#many_tickets)
- [讓票要注意的詐騙](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#ticket-fraud)
- [使用搶票程式會讓自己的帳號被鎖住嗎？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#account_locked)
- [如何恢復拓元的「購票權限」？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#unlock)
- [網頁刷新速度有推薦幾秒刷新一次嗎？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#refresh)
- [搶票的電腦需要多少的網路頻寬才夠？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#bandwidth)
- [使用VPN/代理伺服器(Proxy)來搶票會有用嗎？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#proxy)
- [同一個IP短時間重試被系統視為惡意程式而封鎖怎麼辦？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#ip_blocked)
- [Firefox和chrome搶票上有差距嗎？我看大家基本上都用chrome 很少用Firefox.](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#firefox_vs_chrome)
- [為什麼要設計搶票的機制？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#race_game)
- [為什麼網頁會有驗證碼？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#captcha)
- [你的硬體設備該不該升級？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#hardware)
- [想組一台新的電腦，是不是可以給我一些建議呢？](https://max-everyday.com/2023/02/common-problem-when-you-buy-ticket/#new_compute_suggestion)
</details>

## Extension Privacy 擴充功能隱私權政策

<details>
<summary><code><b>MaxBot Plus擴充功能隱私權政策</b>（點我展開）</code></summary>

### 產品如何收集、使用及分享使用者資料

- 擴充取得會取得特定網頁內容, 並且自動輸入張數。
- 擴充功能會移除特定網頁內容裡已售完的網頁區塊。
- 擴充功能會取得特定網址資訊, 並置換為下一個新的網址。
- 擴充取得會取得特定網頁內容, 判斷為需要重新整理時, 自動刷新頁面。

### 使用者資料的所有分享對象。

- 擴充功能沒有分享使用者資料。

### 擴充功能主要功能：

- 特定的訂票網頁內容, 並且自動輸入張數。
- 移除特定的訂票網頁內容裡已售完的網頁區塊。
- 特定的訂票網址, 自動置換為下一步的新網址。
- 當訂票網頁內容已經無票或沒有符合的關鍵字時, 自動刷新網頁。
- 特定網頁支援驗證碼功能, 需要同時開啟 MaxBot 主程式。
</details>
