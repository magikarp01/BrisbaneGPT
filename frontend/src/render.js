const { ipcRenderer } = require('electron');
const { axios } = require("axois");

const SERVER_URL = "http://127.0.0.1:5000";
(() => {
  axios
    .get(`${SERVER_URL}/`)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
})();

const fileRequest = (requestObject) => {
  axios
    .post(`${SERVER_URL}/file`, requestObject)
    .then((response) => {
      console.log("Server response", response.data);
    })
    .catch((error) => {
      console.error(error);
    })
}

const chatRequest = (requestObject) => {
  axios
    .post(`${SERVER_URL}/chat`)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}

const selectDirectoryButton = document.getElementById('select-dir');
const clearDirectoryButton = document.getElementById('clear-dir');
const chatSubmitButton = document.getElementById('chat-submit');

const fileList = document.getElementById('file-list');
const chatText = document.getElementById('chat-text');
const chatContainer = document.getElementById('messages-container');

selectDirectoryButton.addEventListener('click', () => {
  ipcRenderer.send('open-directory-dialog');
});

ipcRenderer.on('selected-directory', (event, directoryPath) => {
  // Clear the current file list
  fileList.innerHTML = '';

  // Get the directory contents
  const fs = require('fs');

  const fileRequestObject = {
    path: directoryPath
  }
  fileRequest(fileRequestObject);

  chatSubmitButton.addEventListener('click', () => {
    // Add a chat
    const newChat = document.createElement('div');
    newChat.classList.add('bg-blue-500');
    newChat.classList.add('float-right');
    newChat.classList.add('w-3/5');
    newChat.classList.add('mx-4');
    newChat.classList.add('my-2');
    newChat.classList.add('p-4');
    newChat.classList.add('rounded-xl');
    newChat.classList.add('clearfix');

    newChat.textContent = chatText.value;
    chatText.value = '';
    chatContainer.appendChild(newChat);
  });

  ipcRenderer.on('selected-directory', (event, directoryPath) => {
    // Get the directory contents
    const fs = require('fs');

    recListFiles(directoryPath, fileList, fs);
  });

  function recListFiles(path, fileList, fs) {
    console.log(path);
    const itemElement = document.createElement('li');
    if (!fs.statSync(path).isDirectory()) {
      // Base case (file)
      itemElement.textContent = `📃 ${path.split("/").slice(-1)}`;
      itemElement.classList.add('indent-2');
      fileList.appendChild(itemElement);
    } else {
      const dirContents = fs.readdirSync(path);
      itemElement.textContent = `📁 ${path.split("\\").slice(-1)}`
      fileList.appendChild(itemElement);
      // Recursive step
      for (const item of dirContents) {
        recListFiles(`${path}/${item}`, fileList, fs);
      }
    }
  }