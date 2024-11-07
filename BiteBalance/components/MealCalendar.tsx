import { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";
import { Calendar, DateData } from "react-native-calendars";
import { fetchMonthMeals } from "@/api/service";

import { MarkedDates } from "react-native-calendars/src/types";

export default function MealCalendar() {
  const currentDate = new Date();
  // for visualizing marks on days where meals were tracked
  const [trackedDays, setTrackedDays] = useState<MarkedDates>({});
  // currently selected date
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  // data is all pulled in from BE
  const [isLoaded, setIsLoaded] = useState(false);

  // TODO:
  // figure out what we want to do for selected date when switching months
  // auto go to a date in that month or not
  // prevent going forward in time past today's date
  // need to have trackedDays and trackedDays data separate?
  // way of displaying that selectedDays tracked data
  // create db with dates on uploaded images
  // create space for AI info

  // populate information about meal data from current month on startup
  useEffect(() => {
    const getMealData = async () => {
      const formattedDate = formatToMMDDYYYY(selectedDate)

      // receive obj of key dates (MM-DD-YYYY) with value: count
      const response = await fetchMonthMeals(formattedDate);
      const json = await response?.json();

      // from tracked days -> convert to dots on calendar
      const tracked: MarkedDates = {};
      for (const [date, count] of Object.entries(json)) {
        const countInt = parseInt(count as string)
        let [y, m, d] = date.split("-");
        m = m.padStart(2, "0");
        d = d.padStart(2, "0");
        const newDate = `${y}-${m}-${d}`;
        const dayObjs = [];

        for (let i = 0; i < countInt; i++) {
          dayObjs.push({
            key: `meal${i}`,
            color: "green",
            selectedDotColor: "green",
          });
        }
        tracked[newDate] = {
          dots: dayObjs,
          selectedColor: "lightblue",
        };
      }

      // select current day
      const currentDateFormatted = formatToYYYYMMDD(selectedDate)
      tracked[currentDateFormatted] = {
        ...(tracked[currentDateFormatted] || {}),
        ...{ selected: true, selectedColor: "lightblue" },
      };

      setTrackedDays(tracked);
    };

    getMealData();
    setIsLoaded(true);
  }, []);

  const selectDay = (day: DateData) => {
    const currentTrackedDays = { ...trackedDays };
    const selectedDay = currentTrackedDays[day.dateString];

    const currentSelectedDay = selectedDate.toISOString().split("T")[0];
    // need to ensure selected is property on this tracked -> see if trackedDays exists
    if (trackedDays[currentSelectedDay].selected) {
      delete trackedDays[currentSelectedDay].selected;
    }

    // ensure correct date is selected based on if date has meals tracked
    if (selectedDay !== undefined) {
      currentTrackedDays[day.dateString] = {
        ...selectedDay,
        selected: true,
        selectedColor: "lightblue",
      };
    } else {
      currentTrackedDays[day.dateString] = {
        selected: true,
        selectedColor: "lightblue",
      };
    }
    
    setSelectedDate(new Date(day.dateString));
    setTrackedDays(currentTrackedDays);
  };

  const isMonthInFuture = () => {
    // need to make selectedDate a date obj and same with currentDate so that
    // I can use getMonth to do comparison
    // can also just do regex on the ISODateString
    // return selectedDate.getMonth() >=
  };

  const formatToYYYYMMDD = (date: Date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  const formatToMMDDYYYY = (date: Date) => {
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    const year = date.getFullYear();
    return `${month}-${day}-${year}`;
  }

  return (
    <View>
      {isLoaded && (
        <Calendar
          maxDate={currentDate.toISOString().split("T")[0]}
          onDayPress={(day) => {
            selectDay(day);
          }}
          markingType={"multi-dot"}
          markedDates={trackedDays}
          testID={"calendar"}
          // disableArrowRight={isMonthInFuture}
        />
      )}
      <View>
        <Text testID="date-text">
          {selectedDate.toISOString().split("T")[0]}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({});
