from langchain_openai import ChatOpenAI
from educhain import Educhain, LLMConfig
from io import StringIO

from educhain.models.content_models import FlashcardSet  #Importing Educhain classes
from educhain.models.content_models import LessonPlan

llama3 = ChatOpenAI(
    model = "llama-3.3-70b-versatile",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = "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"
)

llama3_config = LLMConfig(custom_model=llama3)
client_llama3 = Educhain(llama3_config)

def get_flashcard_set_as_string(flashcard_set: FlashcardSet) -> str:
    output = StringIO()

    output.write("=" * 80 + "\n")
    output.write(f"Flashcard Set: {flashcard_set.title}\n")
    output.write("=" * 80 + "\n")

    for i, flashcard in enumerate(flashcard_set.flashcards, 1):
        output.write(f"\n{i}. Front: {flashcard.front}\n")
        output.write(f"   Back: {flashcard.back}\n")
        if getattr(flashcard, 'explanation', None):
            output.write(f"   Explanation: {flashcard.explanation}\n")

    output.write("\n" + "=" * 80 + "\n")

    # Optional fields, in case they're dynamically added or defined in extended models
    if getattr(flashcard_set, "learning_adaptations", None):
        output.write(f"\nLearning Adaptations: {flashcard_set.learning_adaptations}\n")
    else:
        output.write("Learning Adaptations: None\n")

    if getattr(flashcard_set, "real_world_applications", None):
        output.write(f"Real-World Applications: {flashcard_set.real_world_applications}\n")
    else:
        output.write("Real-World Applications: None\n")

    if getattr(flashcard_set, "ethical_considerations", None):
        output.write(f"Ethical Considerations: {flashcard_set.ethical_considerations}\n")
    else:
        output.write("Ethical Considerations: None\n")

    return output.getvalue()

flashcard_set = client_llama3.content_engine.generate_flashcards("Python Basics")

flashcard_string = get_flashcard_set_as_string(flashcard_set)  # assuming you have a FlashcardSet instance
print(type(flashcard_set))
print(type(flashcard_string))
print(flashcard_string)

