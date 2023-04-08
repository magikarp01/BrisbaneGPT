const { ipcRenderer } = require('electron');

const selectDirectoryButton = document.getElementById('select-dir');
const fileList = document.getElementById('file-list');

selectDirectoryButton.addEventListener('click', () => {
  ipcRenderer.send('open-directory-dialog');
});

ipcRenderer.on('selected-directory', (event, directoryPath) => {
    // Clear the current file list
    fileList.innerHTML = '';
  
    // Get the directory contents
    const fs = require('fs');
  
    recListFiles(directoryPath, fileList, fs);
});

function recListFiles(path, fileList, fs){
    console.log(path);
    const itemElement = document.createElement('li');
    if(!fs.statSync(path).isDirectory()){
        // Base case (file)
        itemElement.textContent = `📃 ${path.split("/").slice(-1)}`;
        itemElement.classList.add('indent-2');
        fileList.appendChild(itemElement);
    }else{
        const dirContents = fs.readdirSync(path);
        itemElement.textContent = `📁 ${path.split("\\").slice(-1)}`
        fileList.appendChild(itemElement);
        // Recursive step
        for (const item of dirContents) {
            recListFiles(`${path}/${item}`, fileList, fs);
        }
    }
}