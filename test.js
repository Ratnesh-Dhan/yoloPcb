const { dir } = require("console");
const fs = require("fs");
const path = require("path");

const directoryPath = "./ann";

// const file_name = "WhatsApp Image 2025-03-26 at 11.44.01 AM (1).txt";
// const file_path = path.join(directoryPath, file_name);
// const file_content = fs.readFileSync(file_path, "utf8");

const files = fs.readdirSync(directoryPath);
const files_we = [];
files.forEach((element) => {
  const fileNameWithoutExtension = element.substring(
    0,
    element.lastIndexOf(".")
  );
  files_we.push(fileNameWithoutExtension);
});
const image_files = fs.readdirSync("./img");
const image_files_we = [];
image_files.forEach((element) => {
  image_files_we.push(element.substring(0, element.lastIndexOf(".")));
});
console.log(
  `images count ${image_files_we.length}: annotations count ${files_we.length}`
);
const delFiles = files_we.filter((file) => !image_files_we.includes(file));
console.log(delFiles);
// const files = fs.readdirSync(directoryPath);
// console.log(files);

// files.forEach((element) => {
//   const filePath = path.join(directoryPath, element);
//   const fileContent = fs.readFileSync(filePath, "utf8");
//   console.log(`Content of ${element}:`, fileContent);
// });
