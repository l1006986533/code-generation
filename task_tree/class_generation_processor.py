import json
from openai import OpenAI
from pydantic import BaseModel

api_key = 'sk-BGsbjdC7lXQGHgJyh61xf04bBeR1P6uFForzHoXU4jsmWsrx'
client = OpenAI(
    api_key=api_key,
    base_url="https://api.chatanywhere.tech/v1"
)

def class_generation_prompt(current_class, dependencies):
    a = json.loads(get_definition_results())

    s = """Now you are given the definition about one single class. You need to implement it by Java.
        Here is the class you need to implement:
        \n"""
    for i in a:
        if (i["class_name"] == current_class):
            s += str(i)
    s += "\nExist elements that you can use and no need to implement again:"
    for i in range(len(dependencies)):
        s += "\n\nDependency " + str(i + 1) + ":\n"
        for j in a:
            rag_result = rag.query(j["class_name"])
            print(rag_result)
            for k in rag_result:
                pair = k.split('&&&&&')
                key, val = pair[0].split('.')[0], pair[1]
                if key == dependencies[i]:
                    s += k
    s += """\n\nOther tips:
        Assert the package root as com.test.generation, you should concat package definition after that.
        Give the code only, do not give any summary or conclusion in the begin or end of the answer.
        Only generate the single class and its functions I give to you."""

    return s

def llm_generation(content, generation_structure, model_type="gpt-4o-mini", logger=LOG):
    logger.write('--------------asking gpt for--------------\n')
    logger.write(content + '\n')
    completion = client.beta.chat.completions.parse(
        model=model_type,
        messages=[
            {"role": "user", "content": content}
        ],
        response_format=generation_structure
    )
    logger.write('--------------got response--------------\n')
    logger.write(str(completion.choices[0].message.parsed) + '\n')
    return completion.choices[0].message.parsed


class code_generation(BaseModel):
    package: str
    imports: str
    contents: str

def process():
    # 流程： 1. 生成这个类之前，获取dependencies的信息。先检索这个类的依赖有哪些，然后用rag.query得到依赖的相关信息（例如，直接发送源代码，或者只发送函数签名）
    # 2.  构造prompt。prompt包含对这个类的要求，和dependencies的信息
    # 3. 调用大模型生成代码，然后返回代码。返回的代码遵循package--imports--contents的格式
    pass
