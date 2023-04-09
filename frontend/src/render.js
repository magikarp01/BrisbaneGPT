const { ipcRenderer } = require('electron');
const os = require('os');
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

// API call for embedding files
const fileRequest = async (requestObject) => {
  res = await axios.post(`${SERVER_URL}/file`, requestObject).catch((error) => {
    console.error(error);
  });
  return res;
};

// API call for answering chats
const chatRequest = async (requestObject) => {
  res = await axios.post(`${SERVER_URL}/chat`, requestObject).catch((error) => {
    console.error(error);
  });

  return res.data.response;
};

// Buttons
const selectDirectoryButton = document.getElementById('select-dir');
const clearDirectoryButton = document.getElementById('clear-dir');
const chatSubmitButton = document.getElementById('chat-submit');
const clearChatButton = document.getElementById('chat-clear');

// Lists and containers
const fileList = document.getElementById('file-list');
const chatText = document.getElementById('chat-text');
const chatContainer = document.getElementById('messages-container');

// Loading icons
const fileLoader = document.getElementById('file-loader');
const chatLoader = document.getElementById('chat-loader');

// Event listeners
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
    newChat.classList.add('break-words');
    newChat.classList.add('rounded-xl');

    newChat.textContent = chatText.value;
    chatText.value = '';

    const newChatContainer = document.createElement('div');
    newChatContainer.classList.add('clearfix');
    newChatContainer.appendChild(newChat);
    chatContainer.appendChild(newChatContainer);

    // Add loading response
    chatLoader.classList.remove('hidden');

    const requestObject = {
      query: newChat.textContent,
    };
    responseText = await chatRequest(requestObject);
    files = Array();
    for (const f of responseText.matchAll(/{([^}]*)}/g)) {
      files.push(f[1]);
    }
    let i = 0;
    responseText = responseText.replaceAll('\n', '<br>');
    const getFile = () => {
      i += 1;
      return files[i - 1];
    };
    while (responseText.match(/{[^}]*[\\\/]([^}]*)}/g)) {
      responseText = responseText.replace(
        /{[^}]*[\\\/]([^}]*)}/i,
        `<a href="${getFile()}" target="_blank" class="text-blue-500 underline">$1</a>`
      );
    }

    // Remove loading response
    chatLoader.classList.add('hidden');

    // Add response to the chat
    const newResponse = document.createElement('div');
    newResponse.classList.add('bg-gray-300');
    newResponse.classList.add('text-gray-700');
    newResponse.classList.add('w-3/5');
    newResponse.classList.add('mx-4');
    newResponse.classList.add('my-2');
    newResponse.classList.add('p-4');
    newResponse.classList.add('break-words');
    newResponse.classList.add('rounded-xl');
    newResponse.classList.add('clearfix');

    newResponse.innerHTML = responseText;

    const newResponseContainer = document.createElement('div');
    newResponseContainer.classList.add('clearfix');
    newResponseContainer.appendChild(newResponse);

    chatContainer.appendChild(newResponseContainer);
  }
});

// When directory is selected, send it to backend
ipcRenderer.on('selected-directory', async (event, directoryPath) => {
  // Get the directory contents
  const fs = require('fs');

  const requestObject = {
    path: directoryPath,
  };

  // Loading animation
  fileLoader.classList.remove('hidden');
  await fileRequest(requestObject);
  fileLoader.classList.add('hidden');
  indent_counter = 0;
  recListFiles(directoryPath, fileList, fs, indent_counter);
});

// Recursively list out all files in subdirectories
function recListFiles(fpath, fileList, fs, indent_counter) {
  const itemElement = document.createElement('li');
  if (!fs.statSync(fpath).isDirectory()) {
    // Base case (file)
    const itemLink = document.createElement('a');
    itemLink.href = fpath;
    itemLink.target = '_blank';
    itemLink.textContent = `📃 ${fpath
      .split('\\')
      .slice(-1)[0]
      .split('/')
      .slice(-1)}`;

    itemElement.appendChild(itemLink);
    if (indent_counter > 0) {
      itemElement.classList.add(`indent-${indent_counter}`);
    }
    fileList.appendChild(itemElement);
  } else {
    const dirContents = fs.readdirSync(fpath);
    itemElement.textContent = `📁 ${fpath
      .split('\\')
      .slice(-1)[0]
      .split('/')
      .slice(-1)}`;
    if (indent_counter > 0) {
      itemElement.classList.add(`indent-${indent_counter}`);
    }
    fileList.appendChild(itemElement);

    indent_counter += 2;
    // Recursive step
    // First list files
    for (const item of dirContents) {
      if (!fs.statSync(`${fpath}/${item}`).isDirectory()) {
        recListFiles(`${fpath}/${item}`, fileList, fs, indent_counter);
      }
    }
    // Then list folders
    for (const item of dirContents) {
      if (fs.statSync(`${fpath}/${item}`).isDirectory()) {
        recListFiles(`${fpath}/${item}`, fileList, fs, indent_counter);
      }
    }
  }
}

function toggleSlideover() {
  document.getElementById('slideover-container').classList.toggle('invisible');
  document.getElementById('slideover-bg').classList.toggle('opacity-0');
  document.getElementById('slideover-bg').classList.toggle('opacity-50');
  document.getElementById('slideover').classList.toggle('translate-x-full');
}
