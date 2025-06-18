# main.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# --- Pydanticモデルの定義 ---
# POSTリクエストで受け取るデータの型を定義します。
# これにより、FastAPIはリクエストのボディが正しい形式か自動でチェックしてくれます。

class PresentBody(BaseModel):
    """ /present エンドポイント用のリクエストボディ """
    present: str
    sender: str

class DiagnoseBody(BaseModel):
    """ /diagnose エンドポイント用のリクエストボディ """
    name: str
    thing: str


# --- GETメソッドのエンドポイント ---

@app.get("/")
async def root():
    """ ルートURL。簡単な挨拶を返します。 """
    return {"message": "Hello FastAPI!"}


@app.get("/index", response_class=HTMLResponse)
async def get_index_page():
    """
    課題1および課題2のテスト用HTMLページを返します。
    このHTMLには、オリジナルのPOSTメソッド(/diagnose)をテストするためのフォームが含まれています。
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI 課題テストページ</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                font-family: 'Helvetica Neue', 'Arial', 'Hiragino Sans', 'Meiryo', sans-serif;
            }
        </style>
    </head>
    <body class="bg-gray-100 text-gray-800">
        <div class="container mx-auto p-4 md:p-8">
            <header class="bg-blue-500 text-white p-6 rounded-lg shadow-lg mb-8">
                <h1 class="text-3xl font-bold">FastAPI 課題テストページ</h1>
                <p class="mt-2">このページでは、作成したAPIエンドポイントをテストできます。</p>
            </header>

            <!-- 課題1: オリジナルのWebページ表示 -->
            <section class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold border-b-2 border-blue-300 pb-2 mb-4">課題1：オリジナルWebページの表示</h2>
                <p>このページ自体が、GETメソッドでHTMLを返す課題の回答です。</p>
                <p class="mt-2">このHTMLは自由に書き換えて、オリジナルのページを作成してみてください！</p>
            </section>

            <!-- 課題2: オリジナルPOSTメソッドのテスト -->
            <section class="bg-white p-6 rounded-lg shadow-md">
                <h2 class="text-2xl font-semibold border-b-2 border-blue-300 pb-2 mb-4">課題2：オリジナルPOSTメソッド テスト</h2>
                <p class="mb-4">名前と「好きなこと・もの」を入力して、簡単な性格診断を試してみましょう。<br>これは <code>/diagnose</code> エンドポイントにPOSTリクエストを送信します。</p>
                
                <div id="diagnose-form" class="space-y-4">
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700">あなたの名前</label>
                        <input type="text" id="name" name="name" class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" placeholder="例：山田 太郎">
                    </div>
                    <div>
                        <label for="thing" class="block text-sm font-medium text-gray-700">好きなこと・もの</label>
                        <input type="text" id="thing" name="thing" class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" placeholder="例：ラーメン">
                    </div>
                    <button id="submit-btn" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300 shadow-lg">診断する</button>
                </div>

                <div id="result-area" class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200 hidden">
                    <h3 class="font-semibold text-lg">診断結果：</h3>
                    <p id="result-text" class="mt-2 text-gray-700"></p>
                </div>

            </section>
        </div>

        <script>
            // フォームの送信ボタンがクリックされたときの処理
            document.getElementById('submit-btn').addEventListener('click', async () => {
                const nameInput = document.getElementById('name');
                const thingInput = document.getElementById('thing');
                const resultArea = document.getElementById('result-area');
                const resultText = document.getElementById('result-text');

                // 入力値を取得
                const name = nameInput.value;
                const thing = thingInput.value;

                // 入力が空の場合はアラート
                if (!name || !thing) {
                    alert('名前と好きなものを両方入力してください。');
                    return;
                }

                // POSTリクエストに含めるデータ
                const requestBody = {
                    name: name,
                    thing: thing
                };

                // fetch APIを使ってサーバーにPOSTリクエストを送信
                try {
                    const response = await fetch('/diagnose', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(requestBody),
                    });

                    // サーバーからのレスポンスがエラーの場合
                    if (!response.ok) {
                        throw new Error('サーバーとの通信に失敗しました。');
                    }

                    // レスポンスをJSONとして解析
                    const data = await response.json();

                    // 結果を表示
                    resultText.textContent = data.result;
                    resultArea.classList.remove('hidden');

                } catch (error) {
                    // エラーが発生した場合
                    resultText.textContent = 'エラーが発生しました：' + error.message;
                    resultArea.classList.remove('hidden');
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# --- POSTメソッドのエンドポイント ---

@app.post("/present")
async def give_present(item: PresentBody):
    """ 課題の例として提示されたPOSTメソッドの修正版 """
    # Pydanticモデル `PresentBody` を使ってリクエストボディを受け取る
    response_message = f"サーバです。メリークリスマス！{item.sender}さんから {item.present}をありがとう。お返しはキャンディーです。"
    return {"response": response_message}


@app.post("/diagnose")
async def diagnose_character(item: DiagnoseBody):
    """
    課題2：オリジナルのPOSTメソッド
    名前と好きなものを受け取り、簡単な性格診断を返します。
    """
    name = item.name
    thing = item.thing

    # ランダムで診断結果を選択
    diagnoses = [
        f"{name}さん、{thing}が好きなんですね！あなたは情熱的で、周りを明るくする太陽のような人です！",
        f"{thing}が好きな{name}さんは、探求心が旺盛な冒険家タイプ！新しいことに挑戦するのが得意ですね。",
        f"{name}さんが{thing}を選ぶとは、さすがです。あなたは冷静沈着な戦略家。物事をじっくり考えるのが好きですね。",
        f"こんにちは、{name}さん！{thing}がお好きとは、優しい心の持ち主ですね。思いやりがあって、皆から好かれています。",
    ]
    result_message = random.choice(diagnoses)
    
    return {"result": result_message}

