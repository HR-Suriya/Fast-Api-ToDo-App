
# Making A To DO API WITH FAST API & POETRY

## Starting Project

First Run The Command

```markdown
  poetry new fastapi-neon

  cd fastapi-neon
```

## Creating Files And Copying Code

Create main.py File In fastapi_neon folder under fastapi-neon and make sure the selected Interpreter is of poetry

Copy main.py code from [Here](https://github.com/HR-Suriya/Fast-Api-ToDo-App/blob/main/fastapi-neon/fastapi_neon/main.py)

Create settings.py file on same location beside main.py file

Copy settings.py code from [Here](https://github.com/HR-Suriya/Fast-Api-ToDo-App/blob/main/fastapi-neon/fastapi_neon/settings.py)

Create test_main.py File In test folder under fastapi-neon

Copy test_main.py code from [Here](https://github.com/HR-Suriya/Fast-Api-ToDo-App/blob/main/fastapi-neon/tests/test_main.py)

## Installing Dependencies

Now add all the required dependencies

In our case for whole project needed dependencies are listed below:

- python
- fastapi
- sqlmodel
- pytest
- httpx
- uvicorn [Standard]
- psycopg [Binary]

Python is by default installed while creating project

**For installing all other dependencies through poetry run the command:**

```markdown
  > poetry add fastapi sqlmodel pytest httpx "uvicorn[standard]" "psycopg[binary]"
```

## Making A Connection Between Local File And Database

As we are using Neon database so we need to connect to there

Go to Neon Database by clicking [Here](https://console.neon.tech/).
If you have a account sign in through that account or make a new account

- Make a new project

  - It will ask for some details like **Project Name** and **Database Name**.

- After completing the process of making project it will redirect you to dashboard where there will be a section of Branches

- click **view all** on that section and make a new branch by the name of test

- Now you have database ready you just need to make connection from local device for which you must have neon_cli
  - To install neon cli through npm will require Node JS. Download & Install Node JS from [HERE](https://nodejs.org/en)
  - This npm command will install neon cli globally to use on anywhere in your device:

    ```markdown
      > npm i -g neonctl
    ```

  - After Neon Cli is installed authorize yourself by command

    ```markdown
     > neonctl auth
    ```

  - If you want to you can make sure which account you connected to through command

    ```markdown
      > neonctl me
    ```

- Now go back to dashboard and see there is another section of Connection Details
  - Make sure you have selected **main** branch there will be option of **connection string**.
  - Click there it will give many connection option select psql option.
  - section will also contain eye icon to show password for connection.
  - Make .env file to store secret or personal data (Make sure to put .env file name in .gitignore file so env file should not be     uploaded to github)
  - copy the link under psql 'link' and paste it in env file by **DATABASE_URL** name in .env file as shown in env_backup
  - switch branch to from **main** to **test**
  - repeat the process but this time paste it in **TEST_DATABASE_URL** name in .en
  v file as shown in env_backup

## Checking If File Is Working Correctly

- To make sure file is running accurately we do **pytest**.
   To run pytest run command:

    ```markdown
      > poetry run pytest
    ```

  - It will run pytest where all should be passed and none should fail

- To view It Online we will run command:
  
  ```markdown
    > poetry run uvicorn fastapi_neon.main:app --host localhost --port 8000
  ```

  - Then You can visit on file through links:

```markdown
  http://localhost:8000/
    
  http://localhost:8000/docs

  http://localhost:8000/openapi.json
```
