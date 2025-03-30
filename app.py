import streamlit as st
from langchain.memory import ConversationBufferWindowMemory  # Add this import
from langchain.schema import HumanMessage, AIMessage
# from components.chat_ui import render_chat_ui
from llm_connect_memory import qa_chain

# Constants
CSS = """
    <style>
        /* Target Streamlit button more specifically */
        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-size: 24px !important;
            cursor: pointer !important;
            transition: transform 0.2s !important;
            color: #2e7d32 !important;
        }
        
        /* Target hover state specifically */
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            transform: scale(1.1) !important;
            background-color: transparent !important;
        }
        
        /* Target active/focus states */
        div[data-testid="stButton"] button[kind="secondary"]:active,
        div[data-testid="stButton"] button[kind="secondary"]:focus {
            background-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
            border-color: transparent !important;
        }
        
        /* Remove Streamlit's default styles */
        div[data-testid="stButton"] button[kind="secondary"]::before,
        div[data-testid="stButton"] button[kind="secondary"]::after {
            display: none !important;
        }
        
        /* Main container */
        .main-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            padding: 1rem;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 20px;
            padding-left: 20px;
        }
    </style>
"""

# Update the HEADER constant to remove flex-grow and allow space for reset button
HEADER = """
    <div class="main-container">
        <div style='text-align: center; width: 90%;'>
            <h1>🏥 Medical Assistant Bot</h1>
            <p style='font-size: 1.2em; color: #666;'>Your AI-powered healthcare companion</p>
        </div>
    </div>
"""

AUTO_FOCUS_JS = """
    <script>
        function setFocus() {
            var input = window.parent.document.querySelector('input[type=text]');
            if (input) {
                input.focus();
            }
        }
        setFocus();
        setTimeout(setFocus, 100);
        const observer = new MutationObserver(() => {
            setFocus();
        });
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true
        });
    </script>
"""

def init_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_key" not in st.session_state:
        st.session_state.input_key = "user_input_1"
    if "spinner_placeholder" not in st.session_state:
        st.session_state.spinner_placeholder = st.empty()
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(
            k=10,
            return_messages=True,
            memory_key="chat_history"
        )

def clear_input():
    """Toggle input key to clear input field"""
    st.session_state.input_key = "user_input_2" if st.session_state.input_key == "user_input_1" else "user_input_1"

def reset_chat():
    """Reset chat history and input"""
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Reinitialize session state
    init_session_state()
    
    # Clear input
    clear_input()

def handle_user_input(user_message: str) -> str:
    """Process user input and generate response"""
    try:
        # Add user message to memory
        st.session_state.messages.append(HumanMessage(content=user_message))
        
        # Get response from QA chain
        output = qa_chain.invoke({"query": user_message})
        response = output.get("result", "Sorry, I couldn't generate a response.")
        
        # Add AI response to memory
        st.session_state.messages.append(AIMessage(content=response))
        
        # Save to conversational memory
        st.session_state.memory.save_context(
            {"input": user_message},
            {"output": response}
        )
        
        return response
    except Exception as e:
        print(f"Error during QA chain invocation: {e}")
        st.error(f"An error occurred: {e}")
        return None

def handle_input():
    """Handle input submission"""
    if st.session_state[st.session_state.input_key]:
        user_message = st.session_state[st.session_state.input_key]
        
        with st.session_state.spinner_placeholder:
            with st.spinner("Generating response..."):
                response = handle_user_input(user_message)
                if not response:
                    st.error("No response generated. Please try again.")
        clear_input()

def render_chat_ui():
    """Render the chat interface"""
    st.markdown("""
        <div style='display: flex; flex-direction: column; gap: 1.5rem;'>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.markdown("""
                <div style='display: flex; justify-content: flex-start; margin: 0.5rem 0;'>
                    <div style='
                        background-color: #e6f7ff;
                        padding: 1rem;
                        border-radius: 15px;
                        border-top-left-radius: 5px;
                        max-width: 70%;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                        margin-right: auto;
                        margin-left: 1rem;
                    '>
                        <strong>You:</strong> {}</div>
                </div>
            """.format(msg.content), unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown("""
                <div style='display: flex; justify-content: flex-end; margin: 0.5rem 0;'>
                    <div style='
                        background-color: #d9f7be;
                        padding: 1rem;
                        border-radius: 15px;
                        border-top-right-radius: 5px;
                        max-width: 70%;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                        margin-left: auto;
                        margin-right: 1rem;
                    '>
                        <strong>MediBot:</strong> {}</div>
                </div>
            """.format(msg.content), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_ui():
    """Render all UI components"""
    # Add CSS
    st.markdown(CSS, unsafe_allow_html=True)
    
    # Add header
    st.markdown(HEADER, unsafe_allow_html=True)
    
    # Render chat history
    render_chat_ui()
    
    # Create container for input and reset button
    input_container = st.container()
    with input_container:
        # Create two columns for input and reset button
        input_col, reset_col = st.columns([8, 1])
        
        # Add input field
        with input_col:
            st.text_input(
                "Type your message:", 
                key=st.session_state.input_key,
                on_change=handle_input
            )
        
        # Add reset button
        with reset_col:
            if st.button("🔄", 
                         key="reset_chat_btn", 
                         help="Reset Chat",
                         use_container_width=False,  # Add this parameter
                         type="secondary"):          # Add this parameter
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    # Add spinner placeholder
    with st.container():
        st.session_state.spinner_placeholder = st.empty()
    
    # Add auto-focus JavaScript
    st.components.v1.html(AUTO_FOCUS_JS, height=0)

def main():
    """Main application entry point"""
    init_session_state()
    render_ui()

if __name__ == "__main__":
    main()
