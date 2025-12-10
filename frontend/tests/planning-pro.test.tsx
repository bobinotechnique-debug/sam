import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { PlanningProPage } from "../src/pages/PlanningProPage";

describe("PlanningProPage", () => {
  it("renders timeline V2 placeholders and actions", () => {
    render(<PlanningProPage />);

    expect(screen.getByText(/Planning PRO V2/)).toBeInTheDocument();
    expect(screen.getByText(/Timeline avancée/)).toBeInTheDocument();
    expect(screen.getByText(/Conflits & règles/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /auto-assign v1/i })).toBeInTheDocument();
  });
});
