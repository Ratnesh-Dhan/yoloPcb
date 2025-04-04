#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Function to remap class IDs
function remapClassIds(inputText) {
  // Define the class ID mapping
  const classMapping = {
    11: "7",
    7: "3",
    1: "9",
    3: "13",
    12: "10",
  };

  // Split the input text into lines
  const lines = inputText.split("\n");

  // Process each line
  const remappedLines = lines.map((line) => {
    // Trim whitespace and skip empty lines
    const trimmedLine = line.trim();
    if (!trimmedLine) return line;

    // Split the line into parts
    const parts = trimmedLine.split(/\s+/);

    // Check if the first part is a valid class ID
    if (parts.length > 0 && classMapping.hasOwnProperty(parts[0])) {
      // Replace the class ID with the mapped value
      parts[0] = classMapping[parts[0]];
    }

    // Join the parts back together
    return parts.join(" ");
  });

  // Join the lines back into a single string
  return remappedLines.join("\n");
}

// Main function to handle file processing
function processFile(inputFilePath, outputFilePath) {
  try {
    // Read the input file
    const inputText = fs.readFileSync(inputFilePath, "utf8");

    // Remap the class IDs
    const remappedText = remapClassIds(inputText);

    // Write the output file
    fs.writeFileSync(outputFilePath, remappedText);

    console.log(
      `Successfully processed ${inputFilePath}. Output saved to ${outputFilePath}`
    );
  } catch (error) {
    console.error(`Error processing file: ${error.message}`);
    process.exit(1);
  }
}

// Check if script is run directly
if (require.main === module) {
  // Get input and output file paths from command line arguments
  // const args = process.argv.slice(2);

  // if (args.length !== 2) {
  //   console.error("Usage: node script.js <input_file> <output_file>");
  //   process.exit(1);
  // }

  // const [inputFilePath, outputFilePath] = args;
  const inputFilePath = "./ann/WhatsApp Image 2025-03-26 at 11.44.06 AM.txt";
  processFile(inputFilePath, inputFilePath);

  // const files = fs.readdirSync("./ann");
  // files.forEach((element) => {
  //   const withPath = path.join("./ann", element);
  //   processFile(withPath, withPath);
  //   console.log(withPath, " Done");
  // });
}
