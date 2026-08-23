py -m venv labenv  
Set-ExecutionPolicy Unrestricted -Scope LocalMachine
.\labenv\Scripts\Activate.ps1 
 pip install transformers torch  
 pip install fastapi uvicorn