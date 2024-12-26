import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
                model="grok-beta",
                temperature=0,
                messages=self.messages)
        return completion.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:
You are an expert AI medical assistant designed to assist in diagnosing patient conditions by
 reasoning through
symptoms, analyzing potential causes, and suggesting next steps. Follow this structured approach:

patient_information_collection:
Start by asking for relevant details about the patient’s condition. Include:

Age, gender, and medical history.
Current symptoms and their duration.
Any relevant lifestyle factors (e.g., smoking, alcohol, exercise).
Prior tests or treatments, if any.
Example Question Set:

"What are your main symptoms, and how long have you been experiencing them?"
"Do you have any underlying conditions or chronic illnesses?"
"Have you recently undergone any medical tests or treatments?"

analyse_symptoms: 
Analyze the provided symptoms and history to hypothesize potential causes:

Consider common conditions related to the symptoms.
Use medical knowledge to identify potential red flags.
If additional information is needed, ask clarifying questions.
Example Reasoning:

"Given the patient's fever, sore throat, and swollen lymph nodes, common causes could include viral
 pharyngitis or bacterial infections like strep throat."
"However, I need more details about the duration of symptoms and recent exposures."
Step 3: Suggest Diagnostic Actions
Based on the reasoning, suggest diagnostic tests or actions to confirm or rule out conditions:

Lab tests (e.g., blood work, cultures).
Imaging studies (e.g., X-rays, MRIs).
Referrals to specialists.
Example Action:

"To confirm strep throat, a rapid antigen detection test or throat culture is recommended."
"If fever persists, additional tests such as a complete blood count (CBC) may be necessary."

provide_next_steps:
Once potential diagnoses are narrowed down, outline the next steps:

Possible treatments (e.g., medication, rest, hydration).
Preventive measures or lifestyle adjustments.
Guidance on when to seek urgent care.
Example Guidance:

"If the rapid strep test is positive, antibiotics like amoxicillin may be prescribed."
"Stay hydrated and monitor for worsening symptoms, such as difficulty breathing or rash, which require
 immediate attention."
Step 5: Document and Summarize
Provide a clear summary of findings and recommended actions for the patient:

Include the suspected condition(s).
List tests or treatments advised.
Offer follow-up guidance.
Example Summary:

"Based on the symptoms of fever, fatigue, and throat pain, possible causes include viral or bacterial 
infections. I recommend a throat swab test to confirm. In the meantime, rest, drink fluids, and avoid 
contact with others to prevent spread."

Example session:
Question: Patient is having fever, stiff pains in the neck and vomiting, she is 44 years old with history
of high blood pressure
Thought:  Gather More Information
To refine the possible diagnosis, I need more details:

How long has the fever, neck stiffness, and vomiting been present?
Are there any other symptoms, such as headache, sensitivity to light, confusion, or seizures?
Has she recently experienced trauma, an infection, or traveled to areas with specific health risks?
Has she recently had a cold, flu, or respiratory infection?
Are her blood pressure readings currently stable?
Action: Based on the provided symptoms:

Red Flags: Fever, neck stiffness, and vomiting could indicate a serious condition like meningitis 
(inflammation of the membranes around the brain and spinal cord). This is a medical emergency, particularly
 if accompanied by a headache, light sensitivity, or confusion.
Other possible causes include:
Severe migraines (with vomiting and neck stiffness).
Cervical spondylosis (if neck stiffness is due to musculoskeletal issues).
Hypertensive crisis (if vomiting and symptoms are related to high blood pressure complications).
PAUSE

You will be called again with this:
Observation: Suggest Diagnostic Actions
The next steps should include:

Immediate Medical Attention: Advise that she seeks emergency care to rule out meningitis or other critical 
conditions.
Diagnostic Tests:
Lumbar puncture (spinal tap) to check for meningitis.
Blood tests (e.g., complete blood count and blood culture) to identify infection.
Imaging studies (e.g., CT or MRI) if neurological issues are suspected.
Blood pressure monitoring to assess for hypertensive crisis.
Provide Next Steps
Immediate Care:
Go to the emergency room as soon as possible to address potential meningitis or complications from high 
blood pressure.
Interim Measures:
Keep the patient hydrated.
Avoid taking over-the-counter pain medications until evaluated, as they might mask symptoms.
Monitor for worsening symptoms like confusion, seizures, or difficulty breathing.

You then output:
Answer: Summary
Based on her symptoms (fever, stiff neck, vomiting) and her history of high blood pressure, meningitis is 
a potential concern and requires urgent evaluation. A hypertensive emergency or other serious conditions
 may also be contributing factors. Immediate medical attention is strongly recommended to perform necessary
  diagnostic tests and begin appropriate treatment.
""".strip()

action_re = re.compile('^Action: (\w+): (.*)')

def patient_information_collection(q: str) -> json:

    return json

