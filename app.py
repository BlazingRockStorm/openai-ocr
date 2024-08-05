
# https://qiita.com/nabata/items/32d8fac31549491f56eb

from openai import OpenAI
import os
import base64

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

image_path = "./content/example.png"

json_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "address": {
      "type": "string",
    },
    "name": {
      "type": "string",
    },
    "post_code": {
      "type": "string",
    },
  },
  "required": ["address", "name", "post_code"]
}

with open(image_path, "rb") as image_file:  # 画像ファイルまでのパス
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

completion = client.chat.completions.create(
    model="gpt-4o-mini",  # モデルの指定
    messages=[
        {"role": "system", "content": "You are an excellent secretary who responds in Japanese."},
        {"role": "user",
         "content": [
             {"type": "text", "text": """\
## 命令
この画像に表示されている内容について回答してください。
請求先の住所(address), 氏名(name), 郵便番号(post_code)を教えて下さい。

## Output
"""},
             {
                 "type": "image_url",
                 "image_url": {
                     "url": f"data:image/png;base64,{base64_image}"
                 },
             },
         ],
         }
    ],
    functions=[
        {"name": "extract_text", "parameters": json_schema}
    ],
    function_call={"name": "extract_text"},
)

json.loads(completion.choices[0].message.function_call.arguments)