import { Workspace } from "@/components/workspace";
import { allItems } from "@/lib/curriculum";
import { loadItem } from "@/lib/content";
export function generateStaticParams() {
  return allItems.map(({ slug }) => ({ slug }));
}
export const dynamicParams = false;
export default async function LessonPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const data = await loadItem(slug);
  return (
    <Workspace key={`${data.problem.id}:${data.problem.version}`} data={data} />
  );
}
