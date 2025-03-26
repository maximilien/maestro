import io, sys, asyncio, subprocess

import streamlit as st

from streamlit import runtime
from streamlit.web import cli

from src.workflow import Workflow
from cli.common import Console, parse_yaml

sys_stdout = sys.stdout

class StreamlitOutputRedirector:
    def __init__(self, placeholder):
        self.buffer = ""
        self.placeholder = placeholder

    def write(self, text):
        # Define a keyword to selectively redirect
        keyword_to_redirect = "frames/s]"

        # Check if the keyword is present in the text
        if keyword_to_redirect in text:
            # Redirect text containing the keyword to Streamlit
            # sys.__stdout__.write(text) # Testing

            # Split the input string at each "|"
            split_elements = text.split("|")
            left  = split_elements[0].strip() # contains percentage complete
            right = split_elements[2].strip() # contains "frames/s" information
            newText = left + " | " + right
            # self.setText(newText)
            self.buffer += newText
        else:
            # Print text without the keyword to the console
            sys.__stdout__.write(text)

    def flush(self):
        # Display the captured output
        self.placeholder.write(f"###### {self.buffer}") # markdown, write very small
        self.buffer = ""  

    def clear(self):
        # Clear the Streamlit screen by emptying the placeholder
        self.placeholder.empty()

    def setText(self, newText):
        # Write content into placeholder
        # self.placeholder.write(newText) # normal writing
        self.placeholder.write(f"###### {newText}") # markdown, write very small

    def replacePlaceholder(self, newPlaceholder):
         # Replace with the desired placeholder, which may not be initially known
         self.placeholder = newPlaceholder

def create_workflow(agents_yaml, workflow_yaml):
    return Workflow(agents_yaml, workflow_yaml[0])

def deploy_agents_workflow_streamlit(agents_file, workflow_file):
    output = io.StringIO()
    position = 0
    sys.stdout = output

    agents_yaml = parse_yaml(agents_file)
    workflow_yaml = parse_yaml(workflow_file)
    workflow = create_workflow(agents_yaml, workflow_yaml)

    # Set page configuration
    st.set_page_config(
        page_title="Maestro Workflow",
        page_icon="🤖",
        layout="centered"
    )

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to Maestro workflow?"}
        ]

    # Page header
    st.title(f"Maestro workflow: {workflow_yaml[0]['metadata']['name']}")
    st.markdown(f"{workflow_yaml[0]['spec']['template']['prompt']}")

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🤖"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="👤"):
                st.markdown(message["content"])

    # Function to process user input
    async def process_query(query):
        try:
            return await workflow.run()
        except Exception as e:
            return f"An error occurred: {str(e)}"

    # Chat input
    if prompt := st.chat_input(f"{workflow_yaml[0]['spec']['template']['prompt']}"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant", avatar="🔑"):            
            message_placeholder = st.empty()
            # output_redirector = StreamlitOutputRedirector(message_placeholder)
            # #sys.stdout = output_redirector

            # message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")

            # from cli.streamlit_redirect import redirect
            # redirect.stdout(to=message_placeholder, format='markdown')

            # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            # while process.poll() is None:
            #     line = process.stdout.readline()
            #     if not line:
            #         continue
            #     message_placeholder.write(line.strip())
            
            # Process the query
            response = asyncio.run(process_query(prompt))

            # message = output.getvalue()
            # if len(message) > position:
            #     lines = output.getvalue()[position:].splitlines()
            #     for line in lines:
            #         message_placeholder.markdown(f"{line}")
            #     position = len(message)

            # Update the placeholder with the response
            if response.get('final_prompt'):
                message_placeholder.markdown(response['final_prompt'])
            else:
                message_placeholder.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 

if __name__ == '__main__':
    if runtime.exists():
        deploy_agents_workflow_streamlit(sys.argv[1], sys.argv[2])
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(cli.main())