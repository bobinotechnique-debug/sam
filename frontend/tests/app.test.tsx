import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import App from "../src/App";

global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  status: 200,
  json: async () => ({ status: "ok" }),
}) as unknown as typeof fetch;

describe("App", () => {
  it("renders headings and health state", async () => {
    render(<App />);
    expect(screen.getByText(/Codex Starter/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/API healthy/i)).toBeInTheDocument());
  });
});
