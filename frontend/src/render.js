const { ipcRenderer } = require('electron');
const path = require('path');
const axios = require('axios');

const SERVER_URL = 'http://localhost:8000';

(() => {
  axios
    .get(`${SERVER_URL}/`)
    .then((response) => response.data)
    .then((data) => console.log(data))
    .catch((error) => {
      console.error(error);
    });
})();

const fileRequest = async (requestObject) => {
  res = await axios.post(`${SERVER_URL}/file`, requestObject).catch((error) => {
    console.error(error);
  });
  return res;
};

const chatRequest = async (requestObject) => {
  res = await axios.post(`${SERVER_URL}/chat`, requestObject).catch((error) => {
    console.error(error);
  });

  return res.data.response;
};

const selectDirectoryButton = document.getElementById('select-dir');
const clearDirectoryButton = document.getElementById('clear-dir');
const chatSubmitButton = document.getElementById('chat-submit');
const clearChatButton = document.getElementById('chat-clear');

const fileList = document.getElementById('file-list');
const chatText = document.getElementById('chat-text');
const chatContainer = document.getElementById('messages-container');

selectDirectoryButton.addEventListener('click', () => {
  ipcRenderer.send('open-directory-dialog');
});

clearDirectoryButton.addEventListener('click', () => {
  const fileList = document.getElementById('file-list');
  fileList.innerHTML = '';
});

clearChatButton.addEventListener('click', () => {
  while (chatContainer.firstChild) {
    chatContainer.removeChild(chatContainer.firstChild);
  }
});

chatText.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault(); // Prevent the form from submitting
    chatSubmitButton.click(); // Submit the form
  }
});

chatSubmitButton.addEventListener('click', async () => {
  if (chatText.value.length > 0) {
    // Add a chat
    const newChat = document.createElement('div');
    newChat.classList.add('bg-blue-500');
    newChat.classList.add('w-3/5');
    newChat.classList.add('ml-auto');
    newChat.classList.add('my-2');
    newChat.classList.add('h-auto');
    newChat.classList.add('p-4');
    newChat.classList.add('rounded-xl');

    newChat.textContent = chatText.value;
    chatText.value = '';

    const newChatContainer = document.createElement('div');
    newChatContainer.classList.add('clearfix');
    newChatContainer.appendChild(newChat);
    chatContainer.appendChild(newChatContainer);

    // Add response to the chat
    const newResponse = document.createElement('div');
    newResponse.classList.add('bg-gray-300');
    newResponse.classList.add('w-3/5');
    newResponse.classList.add('mx-4');
    newResponse.classList.add('my-2');
    newResponse.classList.add('p-4');
    newResponse.classList.add('rounded-xl');
    newResponse.classList.add('clearfix');

    const requestObject = {
      query: newChat.textContent,
    };
    responseText = await chatRequest(requestObject);
    newResponse.textContent = responseText;

    const newResponseContainer = document.createElement('div');
    newResponseContainer.classList.add('clearfix');
    newResponseContainer.appendChild(newResponse);

    chatContainer.appendChild(newResponseContainer);
  }
});

ipcRenderer.on('selected-directory', async (event, directoryPath) => {
  // Get the directory contents
  const fs = require('fs');

  const requestObject = {
    path: directoryPath,
  };

  await fileRequest(requestObject);

  recListFiles(directoryPath, fileList, fs);
});

function recListFiles(fpath, fileList, fs) {
  const itemElement = document.createElement('li');
  if (!fs.statSync(fpath).isDirectory()) {
    // Base case (file)
    itemElement.textContent = `📃 ${fpath.split(path.sep).slice(-1)}`;
    itemElement.classList.add('indent-2');
    fileList.appendChild(itemElement);
  } else {
    const dirContents = fs.readdirSync(fpath);
    itemElement.textContent = `📁 ${fpath.split(path.sep).slice(-1)}`;
    fileList.appendChild(itemElement);
    // Recursive step
    for (const item of dirContents) {
      recListFiles(`${fpath}/${item}`, fileList, fs);
    }
  }
}
