"use client";
import { useEffect, useState } from "react";
import { readProgress, type LearningState } from "./progress";
export function useProgress() {
  const [state, setState] = useState<LearningState>({});
  useEffect(() => {
    const refresh = () => setState(readProgress());
    refresh();
    addEventListener("storage", refresh);
    addEventListener("mastery-progress", refresh);
    return () => {
      removeEventListener("storage", refresh);
      removeEventListener("mastery-progress", refresh);
    };
  }, []);
  return state;
}
