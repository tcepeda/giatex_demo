'''
run this script to run automatic app
'''


import subprocess
import webbrowser

def run_streamlit_app(port=8559):
    # Run your Streamlit app using subprocess
    subprocess.Popen(["streamlit", "run", "bacia_hidrografica.py", "--server.port", str(port)])
    
    # Open the default web browser to the address of your Streamlit app
    webbrowser.open_new_tab(f"http://localhost:{port}")  # Modify the URL if needed

if __name__ == "__main__":
    run_streamlit_app()
