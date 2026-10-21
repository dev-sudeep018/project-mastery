import { OpenLab } from "@/components/learning";
import { LearningPage } from "@/components/learning-page";
export default function ExplorePage() {
  return (
    <LearningPage title="Open lab" active="explore">
      <h1>Start with “what happens if…”</h1>
      <p className="page-lead">
        Change one variable and look closely. These small experiments connect
        the mathematics to behavior you can see.
      </p>
      <OpenLab />
    </LearningPage>
  );
}
