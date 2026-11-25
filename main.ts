// news-image-20261124: "Sum up 24 November's world news in one image".
// The entry image is entry.png beside this file, drawn programmatically by
// gen_image.py in this same repository (PIL, flat front-page layout, seven
// verified stories of Tuesday 24 November 2026, masthead names the day).
// This program's job is to deliver that image to /output/entry.png.
//
// Node 22, standard library only, no network. Outside the grader's
// container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SRC = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const OUT = join(OUT_DIR, 'entry.png');

// Validate the image against the competition's gate before copying it:
// a whole PNG, at most 1024 by 1024 pixels, at most 1 MiB.
const buf = readFileSync(SRC);
if (buf.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG file');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}
if (buf.length > 1048576) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB cap`);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT);
console.log(`wrote ${OUT} (${width}x${height}, ${buf.length} bytes)`);
