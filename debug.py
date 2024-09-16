from PIL import Image
from IPython.core.display import HTML, display

from engine.utils import ProgramInterpreter
from prompts.gqa import create_prompt
interpreter = ProgramInterpreter(dataset='gqa')
import openai
openai.api_key=""

def execute(image, prompt):
    image.thumbnail((640,640),Image.Resampling.LANCZOS)
    init_state = dict(
        IMAGE=image.convert('RGB')
    )
    display(image)
    result, prog_state, html_str = interpreter.execute(prompt,init_state,inspect=True)
    display(HTML(html_str))