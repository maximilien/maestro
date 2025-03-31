import io, sys, asyncio, subprocess, os, psutil, traceback

import streamlit as st
import streamlit_mermaid as stmd

from src.workflow import Workflow
from cli.common import Console, parse_yaml, read_file

sys_stdout = sys.stdout

global workflow_instance

class StreamlitWorkflowUI:
    def __init__(self, agents_file, workflow_file, prompt='', title='Maestro workflow'):
        self.title = title
        self.prompt = prompt
        self.agents_file = agents_file
        self.workflow_file = workflow_file

        self.agents_yaml = parse_yaml(agents_file)
        self.workflow_yaml = parse_yaml(workflow_file)
        self.workflow = self.__create_workflow(self.agents_yaml, self.workflow_yaml)

    def setup_ui(self):        
        self.__initialize_session_state()
        self.__add_workflow_name_and_files()
        self.__create_workflow_ui()
        self.__add_initial_prompt()
        self.__create_chat_messages()
        self.__create_chat_input()
        self.__add__chat_reset_button()

    # private

    def __add_workflow_name_and_files(self):
        # add line of workflow: title, agents.yaml, and workflow.yaml
        st.markdown(f"### {self.workflow_yaml[0]['metadata']['name']}")
        cols = st.columns(4)
        with cols[0]:
            with st.popover("agents.yaml"):
                st.markdown("## Formatted agents YAML")
                st.code(read_file(self.agents_file), language="yaml", line_numbers=True, wrap_lines=False, height=700)
        with cols[1]:
            with st.popover("workflow.yaml"):
                st.markdown("## Formatted workflow YAML")
                st.code(read_file(self.workflow_file), language="yaml", line_numbers=True, wrap_lines=False, height=700)

    def __add_initial_prompt(self):
        # add text area with initial input text prompt
        st.text_area("Initial prompt", self.prompt, key=f"text_area:{self.title}")

    def __initialize_session_state(self):
        # Initialize session state for chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Welcome to Maestro workflow?"
                }]

    def __add__chat_reset_button(self):
        # Add reset button
        def reset_conversation():
            st.session_state.conversation = None
            st.session_state.chat_history = None
            message_placeholder = st.empty()

        st.button('Reset', on_click=reset_conversation, key=f"reset_button:{self.title}")

    def __create_chat_input(self):
        prompt = st.chat_input(f"{self.workflow_yaml[0]['spec']['template']['prompt']}", key=f"chat_input:{self.title}")
        if prompt:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            # Display assistant response
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking...")

                self.__start_workflow()

                # stream response
                responses = ''
                for response in st.write_stream(StreamlitWorkflowUI.__generate_output):
                    message_placeholder.markdown(response)
                    responses += f"{response}"
                    
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": responses})

    def __create_chat_messages(self):
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

    def __create_workflow_ui(self):
        # create workflow
        global output
        global workflow_instance
        try:
            workflow_instance = self.__create_workflow(self.agents_yaml, self.workflow_yaml[0])
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Unable to create agents: {str(e)}") from e
        
        # add workflow mermaid diagram to page
        st.markdown("")
        st.markdown(f"###### _Sequence diagram of workflow_")
        mermaid_diagram = workflow_instance.to_mermaid()
        stmd.st_mermaid(mermaid_diagram, key=f"mermaid_diagram:{self.title}")

    def __generate_output():
        global output
        global position
        position = 0
        message = output.getvalue()
        if len(message) > position:
            lines = output.getvalue()[position:].splitlines()
            for line in lines:
                yield f"{line}\n\n"
            position = len(message)

    def __start_workflow(self):
        global output
        output = io.StringIO()
        sys.stdout = output
        asyncio.run(workflow_instance.run())

    def __create_workflow(self, agents_yaml, workflow_yaml):
        return Workflow(agents_yaml, workflow_yaml)
