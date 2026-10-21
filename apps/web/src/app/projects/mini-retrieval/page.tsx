import { LearningPage } from "@/components/learning-page";
import { RetrievalProject } from "@/components/retrieval-project";
export default function ProjectPage() {
  return (
    <LearningPage title="Retrieval project" active="projects">
      <RetrievalProject />
    </LearningPage>
  );
}
