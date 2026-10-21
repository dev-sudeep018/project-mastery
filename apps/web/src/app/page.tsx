import { LearningHome } from "@/components/learning";
import { LearningPage } from "@/components/learning-page";
export default function Home() {
  return (
    <LearningPage title="Your learning space" active="home">
      <LearningHome />
    </LearningPage>
  );
}
