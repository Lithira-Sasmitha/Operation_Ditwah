import utils.net
import utils.clients
import utils.http_session
import utils.transport
import utils.session
import os
import pandas as pd
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") # ඔබගේ .env හි ඇත්තේ මෙම නම බව තහවුරු කරගන්න

# Client එක නිර්මාණය කිරීම
client = genai.Client(api_key=api_key)

def run_classifier():
    input_path = "data/Sample Messages.txt"
    output_path = "output/classified_messages.xlsx"

    if not os.path.exists("output"): os.makedirs("output")

    with open(input_path, 'r', encoding='utf-8') as f:
        messages = [line.strip() for line in f.readlines() if line.strip()]

    results = []
    
    # පද්ධතියට ලබා දෙන උපදෙස් (System Instruction)
    system_prompt = "Classify message. Contract: District: [Name] | Intent: [Rescue/Supply/Info/Other] | Priority: [High/Low]"

    print(f"පණිවිඩ {len(messages)} ක් වර්ගීකරණය වෙමින් පවතී...")

    for msg in messages:
        try:
            # Model නම 'gemini-1.5-flash' ලෙස පමණක් යොදා බලන්න
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                config={'system_instruction': system_prompt},
                contents=msg
            )
            
            classification = response.text.strip()
            results.append({"Message": msg, "Classification": classification})
            print(f"සාර්ථකයි: {msg[:30]}...")
            
            # Quota Limit එක වළක්වා ගැනීමට තත්පර 6ක් රැඳී සිටින්න
            time.sleep(6) 
            
        except Exception as e:
            print(f"දෝෂයක්: {e}")
            # 404 දෝෂයක් දිගටම එන්නේ නම් model="gemini-2.0-flash-exp" ලෙස වෙනස් කර බලන්න
            time.sleep(2)

    df = pd.DataFrame(results)
    df.to_excel(output_path, index=False)
    print(f"\nක්‍රියාවලිය අවසන්! වාර්තාව {output_path} හි ඇත.")

if __name__ == "__main__":
    run_classifier()