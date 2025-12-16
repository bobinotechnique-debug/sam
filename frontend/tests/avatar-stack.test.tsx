import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AvatarStack } from "../src/features/planning/components/AvatarStack";

const people = [
  { id: 1, organization_id: 1, full_name: "Alice Smith", primary_role_id: 1, status: "active", email: "a@example.com" },
  { id: 2, organization_id: 1, full_name: "Bob Stone", primary_role_id: 1, status: "active", email: "b@example.com" },
  { id: 3, organization_id: 1, full_name: "Cara Doe", primary_role_id: 1, status: "active", email: "c@example.com" },
  { id: 4, organization_id: 1, full_name: "Dan Poe", primary_role_id: 1, status: "active", email: "d@example.com" },
];

describe("AvatarStack", () => {
  it("renders initials and overflow counter", () => {
    render(<AvatarStack people={people} limit={2} />);
    expect(screen.getByLabelText("Alice Smith")).toBeInTheDocument();
    expect(screen.getByLabelText("Bob Stone")).toBeInTheDocument();
    expect(screen.getByText("+2")).toBeInTheDocument();
  });
});

