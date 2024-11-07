import React from "react";
import { render, waitFor, debug } from "@testing-library/react-native";
import CalendarPage from "./CalendarPage";
import { fetchMonthMeals } from "../../api/service";

const successfulEmptyFetchMonthMealsResponse = {};

const succesfullyCurrentDayResponse = {
  "2024-11-07": 3,
};

jest.mock("../../api/service", () => ({
  fetchMonthMeals: jest.fn(),
}));

describe("Calendar Page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("Calendar displays currently selected date", async () => {
    fetchMonthMeals.mockResolvedValueOnce({
      status: 200,
      json: jest
        .fn()
        .mockResolvedValueOnce(successfulEmptyFetchMonthMealsResponse),
    });

    const { getByTestId, findByText } = render(<CalendarPage />);

    const currentDate = new Date();
    const currentDateFormatted = currentDate.toISOString().split("T")[0];

    const dateTextField = await findByText(currentDateFormatted);

    expect(dateTextField).toBeTruthy();
  });

  test("Calendar displays dots for dates based on fetchMonthMeals response", async () => {
    fetchMonthMeals.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValueOnce(succesfullyCurrentDayResponse),
    });

    const { getByTestId, debug } = render(<CalendarPage />);

    await waitFor(() => {
      const dateWithDots = getByTestId("calendar.day_2024-11-07");
      
      const dotsChild = dateWithDots.props.children[1];

      expect(dotsChild).toBeDefined()
    });
  });
});
