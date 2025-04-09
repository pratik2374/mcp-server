# MCP Server and Tools  
MCP(Model Context Protocol) helps you build agents and complex workflows on top of LLMs. LLMs frequently need to integrate with data and tools, and MCP provides:
- We can update the LLM for current or relevant data that has not yet be known by LLM
- A growing list of pre-built integrations that your LLM can directly plug into.  
- The flexibility to switch between LLM providers and vendors.  
- Best practices for securing your data within your infrastructure. 

# File Structure
- `main.py` - main file to run MCP server
- `Task1 setup` - Folder having individual educhain function and response generating in required format for MCP server
- `Response` - response folder that has all output images and required Pdf


## Overview  
MCP runs on STDIO, where standarized input is given to server and it return standarized output and these are managed by client.
MCP Server and Tools is a project designed to enable seamless interaction between large language models (LLMs) or AI assistants and real-world data, databases, and current news. By leveraging the **Educhain** library, this project provides a robust framework for AI-driven educational tools and services.  

## Features  
### MCP Server  
- Acts as a bridge between LLMs and external data sources.  
- Enables real-time access to databases, news, and other dynamic information.  

### MCP Tools in this project
Currently the tools rely on Groq API and Open Source models but if we want we can use any number of LLM's as per requiremnet
1. **MCQ Generator**: Automatically generates multiple-choice questions based on input topic and number of MCQ needed moreover we can also provide Extra Information or direction that guides the MCQ generation process
2. **Lesson Plan Generator**: Creates structured lesson plans tailored to specific topics or requirements.  
3. **Flashcard Generator**: Produces flashcards for effective learning and revision.  

## Flow of the project 
After installation of **Educhain** library and setting up API's. I made the educhain clinet using LLama model.
Then MCP tools were initialized using asynchronus functions with proper docString so that LLM can choose proper tool and a outpur is generated and returned to LLM for content generation.

## Use Case  
This project allows AI assistants, such as **Claude Desktop**(MCP host here), to utilize MCP Tools for educational purposes. For example:  
- Generating MCQs for quizzes.  
- Preparing lesson plans for teachers or students.  
- Creating flashcards for study sessions.  


## Technology Stack 
- **uv**: For basic installation and to run the application 
- **Educhain Library**: Core library used to build the MCP Server and Tools.  
- **MCP Server**:  Lightweight programs that each expose specific capabilities through the standardized Model Context Protocol

# References:
- [Educhain Library](https://github.com/satvik314/educhain): Core library used to generate educational content
- [MCP Server](https://github.com/modelcontextprotocol/python-sdk):  Used quickstart guide to get started with MCP server and tool


## Contact  
For questions or support, please contact [pratikgond2005@gmail.com].  