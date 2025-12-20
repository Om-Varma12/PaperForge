import os
from openai import OpenAI

def sendRequest(prompt):

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("hf"),
    )

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct:groq",
        messages=[
            {
                "role": "user",
                "content": """You are an expert academic research writer, technical author, and scientific editor.

    Your task is to generate a structured research paper strictly based on the inputs provided.

    CRITICAL RULES:
    1. You MUST return your response in valid JSON format only.
    2. Do NOT include any text outside the JSON object.
    3. Do NOT include markdown, code blocks, comments, or explanations.
    4. Do NOT hallucinate sections not explicitly provided.
    5. Each section must be complete, coherent, and academic in nature.
    6. The writing must be original, formal, and human-like.
    7. If any constraint conflicts, JSON validity is the top priority.

    INPUTS:
    You will receive exactly three inputs:
    - Project Description
    - Number of Pages
    - Sections List

    LENGTH GUIDELINES:
    - Assume 1 page ≈ 450–500 academic words.
    - Total length must scale with page count.
    - Distribute content proportionally across sections.
    - Do NOT mention word counts in the output.

    SECTION RULES:
    - Generate content ONLY for the provided sections.
    - Section names MUST be used exactly as JSON keys.
    - Do NOT repeat content across sections.
    - Maintain logical flow and terminology consistency.

    PARAGRAPH STRUCTURE (MANDATORY FOR ALL SECTIONS):
    - No section may be a single paragraph.
    - Each section must contain 3 to 6 paragraphs.
    - Each paragraph must contain 4 to 6 complete academic sentences.
    - Each paragraph must focus on exactly one coherent sub-idea.
    - Paragraphs must be separated using double line breaks: "\\n\\n".
    - Do NOT use bullet points, numbering, tables, or inline headings.

    SECTION-AWARE FLOW:
    - Introductory sections: context → motivation → problem/gap.
    - Analytical or review sections: distinct themes or approaches per paragraph.
    - Technical sections: logical execution or design flow.
    - Results sections: setup → observation → interpretation.
    - Conclusion sections: summary → implications → future scope.

    OUTPUT FORMAT (STRICT):
    Return a single JSON object in the following structure:

    {
      "Section Name 1": "Paragraph 1\\n\\nParagraph 2\\n\\nParagraph 3",
      "Section Name 2": "Paragraph 1\\n\\nParagraph 2\\n\\nParagraph 3"
    }

    AMOUNT OF PARAGRAPHS:
    1. Introduction: 4 paragraphs
    2. Literature Review: 6-8 paragraphs
    3. Methodology: 7-8 paragraphs
    4. Experimental Results: 6-7 paragraphs
    5. Conclusion: 4 paragraphs
    6. Abstract: 1 big paragraphs
    All these paragraph counts must be strictly followed, and each paragraph must adhere to the paragraph structure rules mentioned above.
    Also the amount of content must be proportional to the number of pages requested. And the number of lines in a paragraph must be between 8 to 10 sentences.

    LOOK, literature review must be 2-3 times the length of introduction, methodology must be longer than literature review, experimental results must be slightly shorter than methodology but longer than literature review, conclusion must be half the length of introduction, and abstract must be a single long paragraph summarizing the entire paper.

    JSON RULES:
    - All keys and values must be valid JSON strings.
    - Escape quotes properly.
    - No trailing commas.
    - Output must be directly parsable.

    SELF-VALIDATION:
    Before finalizing:
    - Confirm every section has multiple paragraphs.
    - Confirm paragraph breaks use "\\n\\n".
    - Confirm no markdown or extra text exists.
    - If validation fails, regenerate internally before output.

    INPUTS TO USE:
    Project Description: AIML Based phishing website detection system which is developed using XGBoost at its core. The system is designed to identify and block phishing websites in real-time, protecting users from potential cyber threats. By leveraging machine learning algorithms, the system can analyze various features of websites to determine their legitimacy. The use of XGBoost allows for efficient processing and accurate predictions, making it a robust solution for combating phishing attacks.
    Number of Pages: 6
    Sections List: ["Abstract", "Introduction", "Literature Review", "Methodology", "Experimental Results", "Conclusion"]
    """
            }
        ],
    )
    print(completion.choices[0].message.content)
    
sendRequest('')