import os
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

from environ import Env
env = Env()

Env.read_env()
API_KEY = env("API_KEY")

# Initialize the OpenAI client for the Hugging Face endpoint
# It's best to handle the API key securely via environment variables
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("API_KEY"),
)

def landing_page(request):
    """ Renders the main landing page template. """
    return render(request, 'index.html')

@csrf_exempt
def execute_code(request):
    """
    Receives code from the frontend, sends it to the Piston API for execution,
    and returns the result.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    try:
        body_data = json.loads(request.body.decode('utf-8'))
        language = body_data.get('language')
        code = body_data.get('code')
        stdin_data = body_data.get('stdin', '') 

        if not code:
            return JsonResponse({'error': 'Code cannot be empty'}, status=400)

        # Fix for stdin echo:
        if stdin_data:
            stdin_data += "\n"

        api_url = 'https://emkc.org/api/v2/piston/execute'
        language_map = {
            "python": "3.10.0",
            "javascript": "18.15.0",
            "c": "10.2.0",
            "cpp": "10.2.0",
            "java": "15.0.2",
            "csharp": "6.12.0",
        }
        
        payload = {
            'language': language,
            'version': language_map.get(language, '*'),
            'files': [{'content': code}],
            'stdin': stdin_data
        }
        
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        # --- THIS IS THE NEW FIX ---
        
        # Get the JSON response from Piston
        result = response.json()
        run_info = result.get('run', {})

        # Check for stdout and replace newlines with <br>
        if run_info and run_info.get('stdout'):
            # Handle both \r\n (Windows) and \n (Unix) newlines
            run_info['stdout'] = run_info['stdout'].replace('\r\n', '<br>').replace('\n', '<br>')
        
        # Do the same for stderr
        if run_info and run_info.get('stderr'):
            run_info['stderr'] = run_info['stderr'].replace('\r\n', '<br>').replace('\n', '<br>')
            
        # --- END OF FIX ---

        # Return the modified run_info object
        return JsonResponse({'run': run_info})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    
    
@csrf_exempt
def ask_ai(request):
    """
    Handles requests to the AI model, intelligently adding context.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    try:
        body_data = json.loads(request.body.decode('utf-8'))
        prompt = body_data.get('prompt')
        code = body_data.get('code', '') 
        language = body_data.get('language', 'text')

        if not prompt:
            return JsonResponse({'error': 'Prompt cannot be empty'}, status=400)

        # --- NEW LOGIC ---
        
        # Keywords that imply the user wants NEW code, not analysis
        NEW_CODE_KEYWORDS = ["write", "create", "generate", "make", "give me"]
        
        # Check if the prompt is asking for new code
        is_new_code_request = any(prompt.lower().startswith(keyword) for keyword in NEW_CODE_KEYWORDS)

        # 1. If the user asks for new code (or the editor is empty),
        #    just send the prompt.
        if is_new_code_request or not code:
            system_prompt = (
                "You are an expert AI pair programmer. "
                "A user has the following request: \"{user_prompt}\"\n\n"
                "Respond directly to the user's request."
            ).format(user_prompt=prompt)
        
        # 2. Else (the user is asking to "explain", "fix", etc.),
        #    send their code as context.
        else:
            system_prompt = (
                "You are an expert AI pair programmer. "
                "A user has provided the following code snippet in {lang}:\n\n"
                "```\n{code_snippet}\n```\n\n"
                "The user's request is: \"{user_prompt}\"\n\n"
                "Respond directly to the user's request, referencing their code."
            ).format(lang=language, code_snippet=code, user_prompt=prompt)
        
        # --- END OF NEW LOGIC ---

        completion = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-480B-A35B-Instruct",
            messages=[{"role": "user", "content": system_prompt}], # Send the chosen prompt
            stream=False,
        )

        ai_response = completion.choices[0].message.content
        return JsonResponse({'response': ai_response})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)