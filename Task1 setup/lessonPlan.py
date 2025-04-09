from langchain_openai import ChatOpenAI
from educhain import Educhain, LLMConfig
from io import StringIO
from educhain.models.content_models import LessonPlan  # adjust import path as needed

llama3 = ChatOpenAI(
    model = "llama-3.3-70b-versatile",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = "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"
)

llama3_config = LLMConfig(custom_model=llama3)
client_llama3 = Educhain(llama3_config)

lesson = client_llama3.content_engine.generate_lesson_plan(
    topic="Quantum Mechanics"
)
def get_lesson_plan_as_string(lesson: LessonPlan) -> str:
    output = StringIO()

    output.write("=" * 80 + "\n")
    output.write(f"Lesson Plan: {lesson.title}\n")
    output.write(f"Subject: {lesson.subject}\n")
    output.write(f"Learning Objectives: {', '.join(lesson.learning_objectives)}\n")
    output.write(f"Lesson Introduction: {lesson.lesson_introduction}\n")
    output.write("=" * 80 + "\n")

    for i, main_topic in enumerate(lesson.main_topics, 1):
        output.write(f"\nMain Topic {i}: {main_topic.title}\n")
        for j, subtopic in enumerate(main_topic.subtopics, 1):
            output.write(f"\n   Subtopic {i}.{j}: {subtopic.title}\n")
            output.write("   Key Concepts:\n")
            for element in subtopic.key_concepts:
                output.write(f"      - {element.type.capitalize()}: {element.content}\n")

            output.write("   Discussion Questions:\n")
            for dq in subtopic.discussion_questions:
                output.write(f"      - {dq.question}\n")

            output.write("   Hands-On Activities:\n")
            for activity in subtopic.hands_on_activities:
                output.write(f"      - {activity.title}: {activity.description}\n")

            output.write("   Reflective Questions:\n")
            for rq in subtopic.reflective_questions:
                output.write(f"      - {rq.question}\n")

            output.write("   Assessment Ideas:\n")
            for assessment in subtopic.assessment_ideas:
                output.write(f"      - {assessment.type.capitalize()}: {assessment.description}\n")

    output.write("\n" + "=" * 80 + "\n")

    # Optionally add these if needed:
    if lesson.learning_adaptations:
        output.write(f"\nLearning Adaptations:\n{lesson.learning_adaptations}\n")
    if lesson.real_world_applications:
        output.write(f"\nReal-World Applications:\n{lesson.real_world_applications}\n")
    if lesson.ethical_considerations:
        output.write(f"\nEthical Considerations:\n{lesson.ethical_considerations}\n")

    return output.getvalue()

lesson_string = get_lesson_plan_as_string(lesson)
print(type(lesson))
print(lesson_string)

