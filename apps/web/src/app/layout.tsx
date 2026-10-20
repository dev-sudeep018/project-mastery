import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "Project Mastery | Learn AI by building",
  description:
    "Free, open-source AI practice. Implement, experiment, and understand, one connected skill at a time.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
