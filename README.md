# RestAPI - Base Model with FastAPI

## Main Steps
1. **Create an environment:**

    **Windows:**
    ```
    python -m venv env
    ```
    **MacOS:**
    ```
    python3 -m venv env
    ```

2. **Environment activate:**

    **Windows:**
    ```
    .\env\Scripts\activate
    ```
    **MacOS:**
    ```
    source env/bin/activate
    ```

3. **Install requirements:**

    ```
    pip install -r requirements.txt
    ```

4. **Run Server:**

    ```
    uvicorn app.main:app --reload
    ```
    or
    ```
    uvicorn <folder>.main:app --reload
    ```

7. **Deactive Environment:**

    ```
    deactivate
    ```

