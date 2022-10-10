# This API project was built in fastAPI.

**setup**

To install the dependencies for this project run pip install -r requirements.txt

before running code, please create a directory called 'data' at the project root

**files**

code used can be found in main.py. tests can be found in test_main.py.

**deployment:**

please run 'pytest' in the terminal at the project root to run tests

This app can can be deployed locally using the following terminal command:
uvicorn app.main:app --reload

A UI to test endpoints can be accessed from the /docs endpoint

**Implemented queries:**

**POST:**
/upload_image

accepts an image in the .jpeg or .png format.

returns a unique identifier for the image

**GET:**
/imagefile

accepts a unique identifier generated by upload_image ending in .jpeg or .png (e.g. a05cb893-4da2-40b7-8148-9e742f5182d5.png)

returns the image in the format specified by the request
