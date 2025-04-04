const fs = require("fs");
const path = require("path");

const txtFiles = fs.readdirSync("./ann");
const imgFiles = fs.readdirSync("./img/new");
// console.group(imgFiles);
const txt_names = [];
txtFiles.forEach((element) => {
  const modifiedName = element.slice(0, element.lastIndexOf("."));
  txt_names.push(modifiedName);
});

const mover = [];
imgFiles.forEach((element) => {
  const modifiedName = element.slice(0, element.lastIndexOf("."));
  if (txt_names.includes(modifiedName)) {
    mover.push(path.join("./img/new", element));
  }
});
console.log(mover);
const destinationFolder = "./img/done"; // Specify the destination folder

// Move each file to the destination folder
mover.forEach((filePath) => {
  const fileName = path.basename(filePath);
  const destinationPath = path.join(destinationFolder, fileName);
  fs.renameSync(filePath, destinationPath);
});
