// news-image-20261124 — "Sum up 24 November's world news in one image".
//
// The image itself (entry.png, next to this file) is drawn by gen_image.py
// in this repository: a PIL front page with seven stories of Tuesday
// 24 November 2026, each verified against live news sources, the masthead
// naming the day. This file only delivers that image to the grader.
//
// Plain Node 22, standard library only, no network. To try it outside the
// grader's container (MAKEFUN_OUTPUT_DIR stands in for /output):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_SIDE = 1024;
const MAX_BYTES = 1024 * 1024;
const PNG_MAGIC = "89504e470d0a1a0a";

function here(): string {
  return dirname(fileURLToPath(import.meta.url));
}

function readEntry(): Buffer {
  const src = join(here(), "entry.png");
  const data = readFileSync(src);
  if (data.subarray(0, 8).toString("hex") !== PNG_MAGIC) {
    throw new Error("entry.png is not a PNG file");
  }
  const w = data.readUInt32BE(16);
  const h = data.readUInt32BE(20);
  if (w > MAX_SIDE || h > MAX_SIDE) {
    throw new Error(`entry.png is ${w}x${h}, over the ${MAX_SIDE}x${MAX_SIDE} cap`);
  }
  if (data.length > MAX_BYTES) {
    throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB cap`);
  }
  return data;
}

function main(): void {
  const data = readEntry();
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const out = join(outDir, "entry.png");
  copyFileSync(join(here(), "entry.png"), out);
  // Prove the copy landed intact before reporting success.
  const landed = readFileSync(out);
  if (landed.length !== data.length) {
    throw new Error(`copy mismatch: wrote ${landed.length} bytes, expected ${data.length}`);
  }
  console.log(
    `wrote ${out} (${data.readUInt32BE(16)}x${data.readUInt32BE(20)}, ${data.length} bytes)`,
  );
}

main();
