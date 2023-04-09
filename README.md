# DirectoryGPT -- A new way to interact with your computer.

DirectoryGPT is a file search engine that allows you to chat with your files using an interactive interface. Made for Bitcamp 2023 at UMD.

## Usage instructions
Executable coming soon! Fow now, follow these instructions to reproduce the desktop application.

### Set up environment:
Make sure you have ```npm```, ```python``` and ```anaconda``` installed!
- Clone the repository
- Create a new conda environment ```conda create -n directorygpt```
- Install requirements ```pip install -r requirements.txt```
- Install node packages ```npm i```
- Set up a [GPT-3.5 OpenAI API key](https://platform.openai.com/docs/models/gpt-3-5), store it in a file named ```.env``` as ```OPENAI_API_KEY="INSERT-KEY-HERE"```

### Set up application:
- On a terminal, run ```python backend/app.py```
- On a separate terminal, run ```npm start```

## Example Usage: Compiling housing information from many sources
![image](https://user-images.githubusercontent.com/47124521/230754542-6fa43c86-0072-48fe-bad6-ecf3d3d7555c.png)

## Example Usage: Interpreting financial information from many reports
![image](https://user-images.githubusercontent.com/47124521/230754741-f2b969a4-ea27-4ecf-9591-62704ce5a6e4.png)

## TODO
- [ ] Create executable 
- [ ] Allow for collaboration in folders 
- [ ] Google Drive/OneDrive integration
