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

import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

export default function CalendarPage() {
  const currentDate = new Date();
  const [selectedDate, setSelectedDate] = useState(
    currentDate.toISOString().split("T")[0]
  );
  // const [isLoaded, setIsLoaded] = useState(false);

  // TODO:
    // figure out what we want to do for selected date when switching months
      // auto go to a date in that month or not
    // prevent going forward in time past today's date
    // need to have trackedDays and trackedDays data separate?
    // way of displaying that selectedDays tracked data
    // create db with dates on uploaded images
    // create space for AI info 

  // when populating this field from db, make sure to add selected for current day
  const [trackedDays, setTrackedDays] = useState<{ [key: string]: {} }>({
    "2024-10-23": {
      dots: [{ key: "breakfast", color: "red", selectedDotColor: "purple" }],
    },
    "2024-10-22": {
      dots: [
        {
          key: "breakfast",
          color: "red",
          selectedDotColor: "purple",
        },
      ],
    },
  });

  useEffect(() => {
    // trying to add current day as a selectedDate in trackedDates
    setTrackedDays({
      ...trackedDays,
      [selectedDate]: { selected: true, selectedColor: "lightblue" },
    });
    console.log("set trackedDays", trackedDays, selectedDate);
    // setIsLoaded(true);
  }, []);

  const selectDay = (day: DateData) => {
    console.log("press day");
    const currentTrackedDays = { ...trackedDays };
    const selectedDay = currentTrackedDays[day.dateString];

    const currentSelectedDay = selectedDate;
    // need to ensure selected is property on this tracked ay -> see if trackedDays exists
    delete trackedDays[currentSelectedDay].selected;

    if (selectedDay !== undefined) {
      console.log("day is tracked");
      currentTrackedDays[day.dateString] = {
        ...selectedDay,
        selected: true,
        selectedColor: "lightblue",
      };
    } else {
      console.log("day is not tracked");
      currentTrackedDays[day.dateString] = {
        selected: true,
        selectedColor: "lightblue",
      };
    }
    console.log("a", currentTrackedDays[day.dateString]);
    setSelectedDate(day.dateString);
    setTrackedDays(currentTrackedDays);
  };

  const isMonthInFuture = () => {
    // need to make selectedDate a date obj and same with currentDate so that
    // I can use getMonth to do comparison 
    // can also just do regex on the ISODateString 
    // return selectedDate.getMonth() >= 
  }

  return (
    <SafeAreaView>
      {/* {isLoaded && ( */}
      <Calendar
        maxDate={currentDate.toISOString().split("T")[0]}
        onDayPress={(day) => {
          selectDay(day);
        }}
        markingType={"multi-dot"}
        markedDates={trackedDays}
        disableArrowRight={isMonthInFuture}
      />
      {/* )} */}
      <View>
        <Text>{selectedDate}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({});
