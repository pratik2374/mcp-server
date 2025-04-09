from langchain_openai import ChatOpenAI
from educhain import Educhain, LLMConfig
from io import StringIO
from educhain.models.qna_models import MCQList

llama3 = ChatOpenAI(
    model = "llama-3.3-70b-versatile",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = "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"
)

llama3_config = LLMConfig(custom_model=llama3)
client_llama3 = Educhain(llama3_config)

questions = client_llama3.qna_engine.generate_questions(
    topic="Quantum Mechanics",
    num=1,
    custom_instructions="Solving qunatum mechanincs problems"
)

def get_all_questions_as_string(mcq_list: MCQList) -> str:
    output = StringIO()

    for q in mcq_list.questions:
        output.write(f"Question: {q.question}\n")
        options_str = "\n".join(f"  {chr(65 + i)}. {option}" for i, option in enumerate(q.options))
        output.write(f"Options:\n{options_str}\n")
        output.write(f"\nCorrect Answer: {q.answer}\n")
        if q.explanation:
            output.write(f"Explanation: {q.explanation}\n")
        output.write("\n")

    return output.getvalue()
  
questions_string = get_all_questions_as_string(questions)

print(type(questions))
print(type(questions_string))
print(questions_string)

