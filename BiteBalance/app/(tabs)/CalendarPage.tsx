import { useState, useEffect } from "react";
import {
  Button,
  Image,
  View,
  Text,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { Calendar, DateData } from "react-native-calendars";
import { fetchMonthMeals } from "@/api/service";

import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

export default function CalendarPage() {
  const currentDate = new Date();
  const [trackedDays, setTrackedDays] = useState<{ [key: string]: {} }>({});
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
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
      const month = (selectedDate.getMonth() + 1).toString().padStart(2, '0');
      let day = selectedDate.getDate().toString().padStart(2, '0');
      const year = selectedDate.getFullYear();
      const formattedDate = `${month}-${day}-${year}`;

      const response = await fetchMonthMeals(formattedDate);
      const json = await response?.json();
      // receive obj of key dates (MM-DD-YYYY) with value: count
      const tracked = {};
      for (const [date, count] of Object.entries(json)) {
        let [y, m, d] = date.split("-");
        m = m.padStart(2, '0')
        d = d.padStart(2, '0')
        console.log(m, d, y)
        const newDate = `${y}-${m}-${d}`;
        const dayObjs = [];

        for (let i = 0; i < count; i++) {
          dayObjs.push({ key: `meal${i}`, color: "green", selectedDotColor: "green" });
        }
        tracked[newDate] = {
          dots: dayObjs,
          selectedColor: "lightblue",
        };
      }

      const currentDateFormatted = `${year}-${month}-${day}`
      tracked[currentDateFormatted] = {
        ...(tracked[currentDateFormatted] || {}),
        ...{selected: true, selectedColor: 'lightblue'}
      }
      setTrackedDays(tracked)

    };
    getMealData();
    setIsLoaded(true);
  }, []);

  const selectDay = (day: DateData) => {
    const currentTrackedDays = { ...trackedDays };
    const selectedDay = currentTrackedDays[day.dateString];

    const currentSelectedDay = selectedDate.toISOString().split("T")[0];
    // need to ensure selected is property on this tracked -> see if trackedDays exists
    delete trackedDays[currentSelectedDay].selected;

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
    console.log("a", currentTrackedDays[day.dateString]);
    setSelectedDate(new Date(day.dateString));
    setTrackedDays(currentTrackedDays);
  };

  const isMonthInFuture = () => {
    // need to make selectedDate a date obj and same with currentDate so that
    // I can use getMonth to do comparison
    // can also just do regex on the ISODateString
    // return selectedDate.getMonth() >=
  };

  return (
    <SafeAreaView>
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
        <Text testID="date-text">{selectedDate.toISOString().split("T")[0]}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({});
