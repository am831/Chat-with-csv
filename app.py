import streamlit as st
from query_data import create_gp_instance, create_oai_instance, query_ai
import asyncio
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

image_path = "./static/csvicon.png"
image = Image.open(image_path)
image_bytes = BytesIO()
image.save(image_bytes, format='PNG')
image_base64 = base64.b64encode(image_bytes.getvalue()).decode()

# Create the Markdown with embedded base64 image
markdown = f"""
<div style="display: flex; align-items: center;">
    <img src="data:image/png;base64,{image_base64}" style="width: 60px;">
    <h1 style="margin-right: 10px;">Query Your CSV With Natural Language</h1>
</div>
"""
st.markdown(markdown, unsafe_allow_html=True)

global_vars = {
    "api_key": None
}

assistant_creation_functions = [
    ("Chat-GPT", create_oai_instance),
    ("Google PaLM", create_gp_instance)
]

async def main():
    st.write("Choose an assistant:")
    selected_choice = st.selectbox("", [""] + [assistant[0] for assistant in assistant_creation_functions])

    if selected_choice:
        st.write("Please enter your API key:")
        global_vars["api_key"] = st.text_input("API Key")

        if global_vars["api_key"]:
            kernel, assistant = None, None
            for assistant_name, create_func in assistant_creation_functions:
                if selected_choice == assistant_name:
                    kernel, assistant = create_func(api_key=global_vars["api_key"])
                    break  # Exit the loop once the correct assistant is found
            
            if kernel and assistant:
                st.write("Please upload your CSV file below.")
                data = st.file_uploader("Upload one or more CSVs", accept_multiple_files=True)
                query = st.text_area("Insert your query")

                if st.button("Submit Query", type="primary") and data is not None:
                    response = await query_ai(kernel=kernel, assistant=assistant, query=query, data=data)
                    st.write(response)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
