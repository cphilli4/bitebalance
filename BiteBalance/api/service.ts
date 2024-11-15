import { UPLOAD_MEAL, MEAL_DATES, MONTH_MEALS, DAY_MEALS } from '../constants/Routes';
import { BACKEND_URL, BACKEND_PORT } from "./config"

const BASE_URL = `${BACKEND_URL}:${BACKEND_PORT}/`

export const uploadImage = async (formData: FormData) => {
  const route = `${BASE_URL + UPLOAD_MEAL}`
  try {
    const response = await fetch(route, {
      method: "POST",
      body: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response;
  } catch (e) {
    console.log('uploadImage Error', e)
  }
};

export const fetchMonthMeals = async (date: string) => {
  const route = `${BASE_URL + MEAL_DATES}?date=${date}`
  try {
    const response = await fetch(route, {
      method: "GET",
    });
    return response;
  } catch (e) {
    console.log('fetchMonthMeals Error', e)
  }
}

export const fetchMealsByDates = async (startDate: string, endDate: string) => {
  const route = `${BASE_URL + MONTH_MEALS}?start_date=${startDate}&end_date=${endDate}`
  try {
    const response = await fetch(route, {
      method: "GET",
    });
    return response;
  } catch (e) {
    console.log('fetchMonthMeals Error', e)
  }
}

export const fetchMealsByDay = async (day: string) => {
  const route = `${BASE_URL + DAY_MEALS}?day=${day}`
  try {
    const response = await fetch(route, {
      method: "GET",
    });
    return response;
  } catch (e) {
    console.log('fetchMonthMeals Error', e)
  }
}
