import os
from markdownify import markdownify as md

import fitz
from PIL import Image

from surya.inference import SuryaInferenceManager
from surya.recognition import RecognitionPredictor

INPUT_DIR = "chapters/"
# The next run will add files to the MkDocs directory so they're ready to go.
OUTPUT_DIR = "site-docs/docs/chapters/"

manager = SuryaInferenceManager()
rec = RecognitionPredictor(manager)

def scan_chapters():
    chapters = [os.path.join(INPUT_DIR, chapter) for chapter in sorted(os.listdir(INPUT_DIR))]

    for chapter in chapters:
        chapter_name = os.path.basename(chapter).replace(".pdf", "")
        markdown_content = ""

        with fitz.open(chapter) as doc:
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                results = rec([img])

                for block in results[0].blocks:
                    markdown_content += md(block.html) + "\n\n"
                
        
        output_file = os.path.join(OUTPUT_DIR, f"{chapter_name}.md")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
                
def main():
    scan_chapters()


