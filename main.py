from mcp.server.fastmcp import FastMCP # Import the FastMCP for MCP server
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from educhain import Educhain, LLMConfig    # Import Educhain
from io import StringIO

from educhain.models.qna_models import MCQList
from educhain.models.content_models import FlashcardSet  #Importing Educhain classes
from educhain.models.content_models import LessonPlan


load_dotenv()                          
# Load the API key from the environment variable
groq_api_key=os.getenv("GROQ_API_KEY")

#Initialization of MCP server
mcp = FastMCP("docs")

# Initialization of Config of Educhain
llama3 = ChatOpenAI(                        #using educhain library along with OpenSource LLM model and Goq API
    model = "llama-3.3-70b-versatile",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = groq_api_key
)

llama3_config = LLMConfig(custom_model=llama3)  #Setup of the client
client_llama3 = Educhain(llama3_config)


# tool to genrate a lesson plan for a given topic
@mcp.tool()
async def generate_Lessonplan(topic:str):
  """
  Generate a well detailed lesson plan for a given topic, duration, garde level and learning objectives.
  lesson plan with main topics, subtopics, key concepts, discussion questions, hands-on activities, reflective questions, and assessment ideas.
  Input Args and format :
      topic: The topic to generate a lesson plan for, eg. "Photosynthesis"
  Returns:
      A well detailed lesson plan.
  """
  detailed_lesson = client_llama3.content_engine.generate_lesson_plan(
      topic=topic,
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
  lesson_string = get_lesson_plan_as_string(detailed_lesson)




# Tool to generate flashcards of a given topic
@mcp.tool()
async def generate_flashcards(topic: str):
    """
    Generate flashcards for a given topic.
    Args:
        topic: The topic to generate flashcards for.

    Returns:
        A list of flashcards.
    """
    flashcard_set = client_llama3.content_engine.generate_flashcards(topic)
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
    flashcard_string = get_flashcard_set_as_string(flashcard_set)
    #returning the string format of questions to client
    return flashcard_string





#tool to generate MCQs of a given topic and has a parameter to give extra information and number to 
#MCQ to be generated
@mcp.tool()  
async def Topicwise_MCQ_Generator(query_topic: str, MCQ_number: int, extra_information:str):
  """
  Generate multiple-choice questions with answer form a given topic with extra information.
  Generate multiple-choice questions with proper question, answer, options and explanation.
    
  Args:
      query_topic: The topic to generate questions for. eg. "Quantum Mechanics"
      MCQ_number: The number of questions to generate. eg. 5
      extra_information: Additional instructions for the question generation. eg. "Solving quantum mechanics problems"

  Returns:
      A list of multiple-choice questions with options, correct answer, and explanation.
  """

  questions = client_llama3.qna_engine.generate_questions(
      topic=query_topic,
      num=MCQ_number,
      custom_instructions=extra_information
  )
    #converts the questions to string format
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
  #returning the string format of questions to client
  return questions_string


#Main function to run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")