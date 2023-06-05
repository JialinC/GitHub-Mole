# LeetHub Research
This is a research project about user GitHub contribution

# Python Version
We provide a convinent tool to query a user's GitHub metrics.
|Methods|Parameters|Metrics|   	|   	|
|---	|---	|---	|---	|---	|
|   	|   	|   	|   	|   	|
|   	|   	|   	|   	|   	|
|   	|   	|   	|   	|   	|
**IN ORDER TO USE THIS TOOL, YOU NEED TO PROVIDE YOUR OWN .env FILE.**
Because we use the [dotenv](https://pypi.org/project/python-dotenv/) package to load environemnt variable.
**YOU ALSO NEED TO PROVIDE YOUR GITHUB PERSONAL ACCESS TOKEN(PAT) IN YOUR .env FILE**
i.e. GITHUB_TOKEN  = 'yourGitHubPAT'
# Nodejs Version
Old queries are written in JS, currently dereprecated.
## Installation
npm -i
## Execution
edit content in main.js to query data
node userGeneralInfo.js

# Python Version
## Installation
pip -r requirements.txt
## Execution
edit content in main.py to query data
python main.py

For this to work, you need to put the input file in the same directory as the .py file because this line:
`const fileStream = fs.createReadStream('test_in.csv')`
decides where to read the input file.
