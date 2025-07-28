import os
import json
import unicodedata
from datetime import datetime
from langdetect import detect, DetectorFactory
from PyPDF2 import PdfReader

DetectorFactory.seed = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PERSONA_FILE = os.path.join(INPUT_DIR, "persona.json")

def load_persona_keywords():
    if not os.path.exists(PERSONA_FILE):
        return {}, []
    with open(PERSONA_FILE, "r", encoding="utf-8") as f:
        persona = json.load(f)
        keywords = []
        if "role" in persona:
            keywords += persona["role"].lower().split()
        if "goal" in persona:
            keywords += persona["goal"].lower().split()
        return persona, list(set(keywords))

def calculate_relevance(text, keywords):
    text = text.lower()
    if not keywords:
        return 0.0
    matches = sum(1 for word in keywords if word in text)
    return round(matches / len(keywords), 2)

def extract_outline(pdf_path, persona_keywords):
    reader = PdfReader(pdf_path)
    outlines = reader.outline

    def parse_outline(items, level=1):
        results = []
        for item in items:
            if isinstance(item, list):
                results.extend(parse_outline(item, level + 1))
            else:
                try:
                    title = unicodedata.normalize("NFKC", item.title)
                    page_num = reader.get_destination_page_number(item) + 1
                    language = detect(title) if len(title.strip()) > 2 else "unknown"
                    relevance = calculate_relevance(title, persona_keywords)
                    results.append({
                        "document": os.path.basename(pdf_path),
                        "page_number": page_num,
                        "section_title": title,
                        "importance_rank": relevance,
                        "language": language,
                        "level": f"H{min(level, 3)}"
                    })
                except:
                    continue
        return results

    return parse_outline(outlines)

def main():
    if not os.path.exists(INPUT_DIR):
        print("❌ Input folder not found.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No PDFs found in input folder.")
        return

    persona, persona_keywords = load_persona_keywords()
    timestamp = datetime.now().isoformat()

    metadata = {
        "input_documents": pdf_files,
        "persona": persona.get("role", "N/A"),
        "job_to_be_done": persona.get("goal", "N/A"),
        "processing_timestamp": timestamp
    }

    sections = []
    for file in pdf_files:
        path = os.path.join(INPUT_DIR, file)
        outlines = extract_outline(path, persona_keywords)
        outlines = sorted(outlines, key=lambda x: x["importance_rank"], reverse=True)
        sections.extend(outlines)

    output = {
        "metadata": metadata,
        "extracted_sections": sections,
        "subsection_analysis": [] 
    }

    output_path = os.path.join(OUTPUT_DIR, "round1b_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Final output saved at: {output_path}")

if __name__ == "__main__":
    main()
