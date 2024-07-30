## 1. Clone the repository
```bash
git clone git@github.com:zakariamohamed123/buy-genius-backend.git
cd buy-genius-backend
```
## 2. Add the upstream remote
```bash
git remote add upstream git@github.com:zakariamohamed123/buy-genius-backend.git
```
## 3. Create a new branch
```bash
git checkout -b <branch-name>
```
## 4. Install dependencies and activate the virtual environment
```bash
pipenv install
pipenv shell
```
## 5. Set Flask environment variables
```bash
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```
## 6. Set up and seed the database
```bash
flask db init
flask db migrate -m "Initial migrate"
flask db upgrade head
python seed.py
```
## 7. Run the server
```bash
flask run
```
## 8. Stage and commit changes
```bash
git add .
git commit -m "<commit-message>"
```
## 9. Push changes to your branch
```bash
git push --set-upstream origin <branch-name>
```
## 10. Create a pull request
Go to the original repository on GitHub.
Switch to the branch you just pushed.
Create a pull request with your changes and select a reviewer.
You are done!
