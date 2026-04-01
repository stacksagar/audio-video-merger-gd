#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const { exec } = require("node:child_process");
const { promisify } = require("node:util");

const execAsync = promisify(exec);

/**
 * Merge videoplayback files sequentially in pairs
 * Place files in ../input directory
 * Output goes to ../output directory
 */

function findVideoFiles(inputDir) {
  const files = fs.readdirSync(inputDir);
  const pattern = /^videoplayback\s*\((\d+)\)\.mp4$/i;

  const videoFiles = [];

  files.forEach((file) => {
    const match = file.match(pattern);
    if (match) {
      videoFiles.push({
        name: file,
        number: Number.parseInt(match[1], 10),
      });
    }
  });

  // Sort by number
  videoFiles.sort((a, b) => a.number - b.number);
  return videoFiles.map((f) => f.name);
}

async function mergeVideos(file1, file2, output, inputDir, outputDir) {
  const cmd = `ffmpeg -i "${path.join(inputDir, file1)}" -i "${path.join(inputDir, file2)}" -c:v copy -c:a aac -shortest -y "${path.join(outputDir, output)}"`;

  try {
    await execAsync(cmd);
    return true;
  } catch (error) {
    console.error(`Error merging ${file1} + ${file2}:`, error.message);
    if (error.stderr) {
      console.error("ffmpeg stderr:", error.stderr);
    }
    return false;
  }
}

function parseArguments(args) {
  let dryRun = false;
  let className = "";
  let startNum = 1;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--dry-run":
        dryRun = true;
        break;
      case "--class":
        className = args[++i];
        break;
      case "--start":
        startNum = Number.parseInt(args[++i], 10);
        break;
      case "--help":
      case "-h":
        showHelp();
        process.exit(0);
    }
  }

  return { dryRun, className, startNum };
}

function showHelp() {
  console.log(`
Usage: node merge_sequential.js [options]

Options:
  --dry-run              Show what would be merged without actually merging
  --class <name>         Class name prefix for output files (e.g., 'classA')
  --start <number>       Starting number for output files (default: 1)
  -h, --help             Show this help message
            `);
}

function createPairs(videoFiles, className, startNum) {
  const pairs = [];
  for (let i = 0; i < videoFiles.length; i += 2) {
    if (i + 1 < videoFiles.length) {
      const file1 = videoFiles[i];
      const file2 = videoFiles[i + 1];

      // Create output filename with class prefix and sequential numbering
      const outputNum = startNum + Math.floor(i / 2);
      const prefix = className ? `${className}_` : "";
      const output = `${prefix}${outputNum}.mp4`;

      pairs.push({ file1, file2, output });
    } else {
      console.log(
        `\nWarning: ${videoFiles[i]} has no pair (odd number of files)`,
      );
    }
  }
  return pairs;
}

async function checkFfmpeg() {
  try {
    await execAsync("ffmpeg -version");
    return true;
  } catch (error) {
    console.log(
      "\nError: ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.",
    );
    return false;
  }
}

async function askConfirmation() {
  const readline = require("node:readline");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const answer = await new Promise((resolve) => {
    rl.question("\nProceed with merging? (y/N): ", resolve);
  });
  rl.close();

  return answer.toLowerCase() === "y";
}

async function processPairs(pairs, inputDir, outputDir) {
  let successCount = 0;
  for (let i = 0; i < pairs.length; i++) {
    const pair = pairs[i];
    console.log(
      `\n[${i + 1}/${pairs.length}] Merging ${pair.file1} + ${pair.file2}...`,
    );

    if (
      await mergeVideos(
        pair.file1,
        pair.file2,
        pair.output,
        inputDir,
        outputDir,
      )
    ) {
      console.log(`  ✅ Created ${pair.output}`);
      successCount++;
    } else {
      console.log(`  ❌ Failed to merge ${pair.file1} + ${pair.file2}`);
    }
  }
  return successCount;
}

async function main() {
  const args = process.argv.slice(2);
  const { dryRun, className, startNum } = parseArguments(args);

  // Set up directories
  const scriptDir = path.dirname(__filename);
  const inputDir = path.join(scriptDir, "..", "input");
  const outputDir = path.join(scriptDir, "..", "output");

  // Create directories if they don't exist
  fs.mkdirSync(inputDir, { recursive: true });
  fs.mkdirSync(outputDir, { recursive: true });

  // Find video files
  const videoFiles = findVideoFiles(inputDir);

  if (videoFiles.length === 0) {
    console.log(`No videoplayback files found in ${inputDir}!`);
    console.log(
      "Please place your videoplayback files in the input directory.",
    );
    console.log('Files should be named like: "videoplayback (1).mp4"');
    process.exit(1);
  }

  console.log(`Found ${videoFiles.length} videoplayback files in ${inputDir}:`);
  videoFiles.forEach((file, i) => {
    console.log(`  ${i + 1}. ${file}`);
  });

  // Create pairs
  const pairs = createPairs(videoFiles, className, startNum);

  if (pairs.length === 0) {
    console.log("\nNo pairs to merge!");
    process.exit(1);
  }

  console.log(`\nWill create ${pairs.length} merged files in ${outputDir}:`);
  pairs.forEach((pair) => {
    console.log(`  ${pair.file1} + ${pair.file2} → ${pair.output}`);
  });

  if (dryRun) {
    console.log("\nDry run complete. Use without --dry-run to actually merge.");
    return;
  }

  // Check if ffmpeg is installed
  if (!(await checkFfmpeg())) {
    process.exit(1);
  }

  // Ask for confirmation
  if (!(await askConfirmation())) {
    console.log("Cancelled.");
    return;
  }

  // Merge pairs
  const successCount = await processPairs(pairs, inputDir, outputDir);
  console.log(
    `\nDone! Successfully merged ${successCount}/${pairs.length} pairs.`,
  );
  console.log(`Output files are in: ${outputDir}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
