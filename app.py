import html
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import PyPDF2
import io
from PIL import Image

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

genai.configure(api_key="enter your gemini api key")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return str(e)

def analyze_health_data(text, language="Russian"):
    try:
        if language == "English":
            prompt = f"""Analyze this health data and format the output as follows:

            Patient Data: {text}

            Structure your response in these categories:
            1. Diagnosis:
            - List key findings
            - Include severity levels

            2. Recommendations:
            - Urgent actions (if any)
            - General recommendations
            - Lifestyle changes

            3. Additional Analysis:
            - Risk factors
            - Preventive measures
            """
        else:
            prompt = f"""Проанализируйте эти данные о здоровье и структурируйте ответ следующим образом:

            Данные пациента: {text}

            Диагноз:
            - Основные находки
            - Степень тяжести

            Рекомендации:
            - Срочные действия (если требуются)
            - Общие рекомендации
            - Изменения образа жизни

            Дополнительный анализ:
            - Факторы риска
            - Профилактические меры
            """
        response = model.generate_content(prompt)
        return response.text.replace('*', '')
    except Exception as e:
        return str(e)

def analyze_health_image(image_bytes, language="Russian"):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        if language == "English":
            prompt = f"""Analyze this medical image and structure your response as follows:

            1. Visual Analysis:
            - Key observations
            - Visible symptoms

            2. Recommendations:
            - Immediate actions
            - Further tests needed
            - General advice

            3. Considerations:
            - Potential risks
            - Additional notes
            """
        else:
            prompt = f"""Проанализируйте это медицинское изображение и структурируйте ответ следующим образом:

            Визуальный анализ:
            - Ключевые наблюдения
            - Видимые симптомы

            Рекомендации:
            - Немедленные действия
            - Необходимые дополнительные обследования
            - Общие советы

            Дополнительно:
            - Потенциальные риски
            - Важные замечания
            """
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content([prompt, image])
        return response.text.replace('*', '')
    except Exception as e:
        return str(e)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'})
        
        pdf_file = request.files['pdf']
        language = request.form.get('language', 'Russian')
        
        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'})

        pdf_content = pdf_file.read()
        text = extract_text_from_pdf(io.BytesIO(pdf_content))
        
        if not text:
            return jsonify({'error': 'Could not extract text from PDF'})


        result = analyze_health_data(text, language)
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'})
        
        image_file = request.files['image']
        language = request.form.get('language', 'Russian')
        
        if image_file.filename == '':
            return jsonify({'error': 'No file selected'})

        image_bytes = image_file.read()

        result = analyze_health_image(image_bytes, language)
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})

# Add chat handling
@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form.get('message', '')
        language = request.form.get('language', 'Russian')
        file = request.files.get('file')

        file_content = ""
        if file:
            if file.filename.lower().endswith('.pdf'):
                pdf_content = file.read()
                file_content = extract_text_from_pdf(io.BytesIO(pdf_content))
            elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes))
                if language == 'English':
                    chat_prompt = f"""You are an AI health assistant. Analyze the provided image and message.
                    Message: {message}
                    Provide a detailed response in English."""
                else:
                    chat_prompt = f"""Вы - ассистент по вопросам здоровья. Проанализируйте предоставленное изображение и сообщение.
                    Сообщение: {message}
                    Предоставьте подробный ответ на русском языке."""
                
                response = model.generate_content([chat_prompt, image])
                return jsonify({'response': response.text})

        if language == 'English':
            chat_prompt = f"""You are an AI health assistant. Provide helpful and informative responses about health-related topics.
            
            User message: {message}
            {f'Document content: {file_content}' if file_content else ''}"""
        else:
            chat_prompt = f"""Вы - ассистент по вопросам здоровья. Предоставьте полезные и информативные ответы.
            
            Сообщение пользователя: {message}
            {f'Содержание документа: {file_content}' if file_content else ''}"""

        response = model.generate_content(chat_prompt)
        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
