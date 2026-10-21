import { PathList } from "@/components/learning";
import { LearningPage } from "@/components/learning-page";
import { paths } from "@/lib/curriculum";
export const dynamicParams = false;
export function generateStaticParams() {
  return paths.map(({ slug }) => ({ slug }));
}
export default async function PathPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return (
    <LearningPage title="Guided paths" active="paths">
      <h1>{paths.find((path) => path.slug === slug)?.title}</h1>
      <PathList slug={slug} />
    </LearningPage>
  );
}
