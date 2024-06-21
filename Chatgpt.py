import openai


def openai_chatgpt_function():
    question="西游记是谁写的？"
    print("问题:{}".format(question))
    openai_url="https://api.gptsapi.net/v1"   #可以替换为任何代理的接口
    OPENAI_API_KEY="sk-iCt1bdbf93860981a10854b437890479fa188c02d57l6lSL"  # openai官网获取key
    openai.api_key = OPENAI_API_KEY
    openai.api_base = openai_url
    response = openai.ChatCompletion.create(
        model="gpt-4o",messages=[{"role": "user", "content": question}],stream=False)
    print("完整的响应结果:{}".format(response))
    answer = response.choices[0].message.content
    print("答案:{}".format(answer))

if __name__ == "__main__":
    openai_chatgpt_function()  # 利用openai正常调用