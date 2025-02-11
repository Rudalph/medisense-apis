from flask import Flask, request, jsonify
from groq import Groq
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


groq_api_key="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"


def recommendations_on_parameters(question):
    try:
        logger.info("Starting recommendations function")
        complete_response = ""
        client = Groq(api_key=groq_api_key)
        
        logger.info("Making API call to Groq")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Changed model name
            messages=[
                {
                    "role": "user",
                    "content": question
                },
            ],
            temperature=1,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                complete_response += chunk.choices[0].delta.content
        
        logger.info(f"Generated response: {complete_response}")
        return complete_response
    except Exception as e:
        logger.error(f"Error in recommendations_on_parameters: {str(e)}")
        raise  # Re-raise the exception to be caught by the route handler


def recommendations():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        question = request.json.get('question')
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        logger.info(f"Received question: {question}")
        
        response = recommendations_on_parameters(question)
        if not response:
            return jsonify({'error': 'No response generated'}), 400
            
        logger.info(f"Generated response: {response}")
        
        recommendations = response.strip()
        cleaned_response = (response
            .replace('*', '')
            .replace('+', '')
            .replace('	', '')  # Remove tabs
            .replace('  ', ' ')  # Remove double spaces
            .strip())
        
        lines = cleaned_response.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        final_response = '\n\n'.join(cleaned_lines)
        
        return jsonify({'recommendations': final_response}), 200
        
    except Exception as e:
        logger.error(f"Error in generate_recommendations: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400
