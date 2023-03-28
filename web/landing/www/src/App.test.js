import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import { describe, test, expect } from "@jest/globals";
import App from "./App";

describe("App", () => {
  test("renders learn react link", () => {
    render(<App />);
    const linkElement = screen.getByText(/A new way to read with AI bot/i);
    expect(linkElement).toBeInTheDocument();
  });
});
