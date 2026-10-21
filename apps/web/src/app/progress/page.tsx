import { ProgressView } from "@/components/learning";
import { LearningPage } from "@/components/learning-page";
export default function ProgressPage() {
  return (
    <LearningPage title="Your progress" active="progress">
      <ProgressView />
    </LearningPage>
  );
}
