# Brisbane (aka DirectoryGPT) -- A new way to interact with your filesystem.

If your files could talk, what would they say? Ask your old code to explain itself, your CS project to tell you its requirements, or a folder full of textbooks to summarize themselves—with Brisbane.

Brisbane is a file search engine that allows you to chat with your files using an interactive interface. Made for Bitcamp 2023 at UMD.

## Usage instructions
Distributable Image coming soon! Fow now, follow these instructions to reproduce the desktop application locally.

### Set up environment:
Make sure you have ```npm```, ```python``` and ```anaconda``` installed!
- Clone the repository
- Create a new conda environment ```conda create -n directorygpt python=3.8```
- Activate the conda environment ```conda activate directorygpt```
- Install requirements ```pip install -r requirements.txt```
- Install node packages in `/frontend` directory: ```npm i```
- Set up a [GPT-3.5 OpenAI API key](https://platform.openai.com/docs/models/gpt-3-5), store it in a file named ```.env``` as ```OPENAI_API_KEY="INSERT-KEY-HERE"```

### Set up application:
- On a terminal, run ```python backend/app.py```
- On a separate terminal, change directory to `/frontend` and run ```npm start```

## Flow of Information
![Brisbane Flowchart](https://user-images.githubusercontent.com/47124521/230788615-d9ad7a55-f50c-46aa-ba26-129d0cd8d54b.png)

## Example Usage: Compiling housing information from many sources
![image](https://user-images.githubusercontent.com/47124521/230754542-6fa43c86-0072-48fe-bad6-ecf3d3d7555c.png)

## Example Usage: Interpreting financial information from many reports
![image](https://user-images.githubusercontent.com/47124521/230754741-f2b969a4-ea27-4ecf-9591-62704ce5a6e4.png)

## TODO
- [ ] Create executable 
- [ ] Allow for collaboration in folders 
- [ ] Google Drive/OneDrive integration
