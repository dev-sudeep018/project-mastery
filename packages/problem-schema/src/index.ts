import { z } from "zod";

export const ProblemSchema = z.strictObject({
  schema_version: z.literal(1),
  id: z.string().regex(/^[mdep][0-9]{2,5}$/),
  kind: z.enum(["lesson", "project"]).default("lesson"),
  slug: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
  version: z.number().int().positive(),
  title: z.string().min(5).max(100),
  summary: z.string().min(20).max(300),
  domain: z.enum(["foundations", "deep-learning", "engineering"]),
  difficulty: z.enum(["beginner", "intermediate", "advanced"]),
  skills: z.array(z.string().min(1)).min(1),
  prerequisites: z.array(z.string().regex(/^[mde][0-9]{2,5}$/)),
  assumed_knowledge: z.array(z.string().min(1)),
  runtime: z.strictObject({
    engine: z.literal("pyodide"),
    packages: z.tuple([z.literal("numpy")]),
  }),
  evaluation: z.strictObject({
    entrypoint: z.string().regex(/^[a-z_][a-z_0-9]*$/),
    absolute_tolerance: z.number().positive(),
    relative_tolerance: z.number().positive(),
  }),
  estimated_minutes: z.number().int().min(1).max(240),
  status: z.enum(["draft", "validated"]),
  author: z.string().min(1),
  license: z.literal("CC-BY-SA-4.0"),
  code_license: z.literal("Apache-2.0"),
  attribution: z.array(z.string()),
});
export type Problem = z.infer<typeof ProblemSchema>;

export const LessonSchema = z.strictObject({
  intro: z.string().min(20),
  task: z.string().min(20),
  signature: z.string().min(3),
  requirements: z.array(z.string().min(10)).min(3),
  examples: z
    .array(
      z.strictObject({
        name: z.string().min(1),
        input: z.string().min(1),
        output: z.string().min(1),
      }),
    )
    .min(3),
  hints: z
    .array(
      z.strictObject({ title: z.string().min(1), body: z.string().min(10) }),
    )
    .min(2),
  explanation: z.array(z.string().min(20)).min(2),
  formula: z.string().nullable(),
  test_count: z.number().int().min(10).max(40),
  sample_count: z.literal(3),
});
export type Lesson = z.infer<typeof LessonSchema>;
export type LearningItem = {
  problem: Problem;
  lesson: Lesson;
  starter: string;
  solution: string;
};

export function validateCatalog(problems: Problem[]) {
  const ids = new Set<string>();
  const slugs = new Set<string>();
  for (const problem of problems) {
    if (ids.has(problem.id) || slugs.has(problem.slug))
      throw new Error(`Duplicate problem: ${problem.id}/${problem.slug}`);
    ids.add(problem.id);
    slugs.add(problem.slug);
  }
  const visiting = new Set<string>();
  const visited = new Set<string>();
  const byId = new Map(problems.map((p) => [p.id, p]));
  function visit(id: string) {
    if (visiting.has(id)) throw new Error(`Prerequisite cycle at ${id}`);
    if (visited.has(id)) return;
    const problem = byId.get(id);
    if (!problem) throw new Error(`Missing prerequisite: ${id}`);
    visiting.add(id);
    for (const prerequisite of problem.prerequisites) visit(prerequisite);
    visiting.delete(id);
    visited.add(id);
  }
  for (const id of ids) visit(id);
}
