import React from "react";
import { render, waitFor, debug } from "@testing-library/react-native";
import MealCalendar from "./MealCalendar";
import { fetchMonthMeals } from "../api/service";

const successfulEmptyFetchMonthMealsResponse = {};

const succesfullyCurrentDayResponse = {
  "2024-12-05": 3,
};

jest.mock("../api/service", () => ({
  fetchMonthMeals: jest.fn(),
}));

describe("MealCalendar Page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });


  test("Calendar displays dots for dates based on fetchMonthMeals response", async () => {
    fetchMonthMeals.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValueOnce(succesfullyCurrentDayResponse),
    });

    const { getByTestId } = render(<MealCalendar />);

    await waitFor(() => {
      const dateWithDots = getByTestId("calendar.day_2024-12-05");
      
      const dotsChild = dateWithDots.props.children[1];

      expect(dotsChild).toBeDefined()
    });
  });
});
