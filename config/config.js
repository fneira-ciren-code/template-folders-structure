import path from "node:path";
import fs from "node:fs";
import fileurl from "node:url";
import dotenv from "dotenv";

dotenv.config();

const __dirname = path.dirname(fileurl.fileURLToPath(import.meta.url));
export const BASE_DIR = path.resolve(__dirname, "..");

const settings = JSON.parse(fs.readFileSync(path.join(BASE_DIR, "config", "settings.json"), "utf-8"));

// Global Constants (SCREAMING_SNAKE_CASE)
export const DIR_DATA_RAW = path.join(BASE_DIR, settings.PATHS.DATA_RAW);
export const DIR_DATA_PROCESSED = path.join(BASE_DIR, settings.PATHS.DATA_PROCESSED);
export const API_SECRET_KEY = process.env.API_SECRET_KEY || "";