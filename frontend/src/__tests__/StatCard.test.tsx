import { render, screen } from "@testing-library/react";
import { StatCard } from "@/components/StatCard";
import { BookOpen } from "lucide-react";

describe("StatCard", () => {
  it("renders label and value", () => {
    render(<StatCard label="Books Available" value={42} icon={BookOpen} />);
    expect(screen.getByText("Books Available")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });
});
