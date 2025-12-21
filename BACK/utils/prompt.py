import textwrap


def prompt_generator(overview):
    prompt = textwrap.dedent("""
You are an expert academic research writer and scientific editor.

Your task is to generate a complete, publication-quality research paper STRICTLY based on the inputs provided.

Also just give me the text, there is no need to give any additional explanations, like "Here is the generated research paper".
or something written in ( ) brackets. or anything else.
I just want the pure text of the research paper.

Project Description:
{overview}
""").format(
        overview=overview
    )

    return {
        "status": "done",
        "prompt": prompt
    }
