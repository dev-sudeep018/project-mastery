"use client";
import Editor, { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor/editor/editor.api";
import "monaco-editor/languages/definitions/python/register";

// Bundle the ESM source so lockfile overrides also update embedded dependencies.
// Copying Monaco's prebuilt AMD distribution would retain its bundled sanitizer.
globalThis.MonacoEnvironment = {
  getWorker: () => new Worker("/editor.worker.js", { type: "module" }),
};
loader.config({ monaco });
export default Editor;
