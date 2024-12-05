import { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import { fetchMealsByDates, fetchMealsByDay } from "@/api/service";

import { Calendar, DateData } from "react-native-calendars";
import { MarkedDates } from "react-native-calendars/src/types";
import Accordion from "react-native-collapsible/Accordion";
import { Image } from "expo-image";

const formatToYYYYMMDD = (date: Date) => {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  return `${year}-${month}-${day}`;
};

const formatToMMDDYYYY = (date: Date) => {
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  const year = date.getFullYear();
  return `${month}-${day}-${year}`;
};

const blurhash =
  "|rF?hV%2WCj[ayj[a|j[az_NaeWBj@ayfRayfQfQM{M|azj[azf6fQfQfQIpWXofj[ayj[j[fQayWCoeoeaya}j[ayfQa{oLj?j[WVj[ayayj[fQoff7azayj[ayj[j[ayofayayayj[fQj[ayayj[ayfjj[j[ayjuayj[";

type MealData = {
  created_at: string;
  label: string;
  url: string;
  meal_data: {
    contents: string[];
    nutrition_value: string;
  };
  id: string;
};

function MealCard({ meal }: { meal: MealData }) {
  return (
    <View>
      <Text>Label: {meal.label}</Text>
      <Text>url: {meal.url}</Text>
      <View>
        <Text>Contents:</Text>
        <FlatList
          data={meal.meal_data.contents}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => <Text>{item}</Text>}
        />
      </View>
      <Text>Nutritional Value: {meal.meal_data.nutrition_value}</Text>
    </View>
  );
}

function MealInfoView({ selectedDate }: { selectedDate: Date }) {
  const [mealData, setMealData] = useState<MealData[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  const [activeSections, setActiveSections] = useState<number[]>([0]);

  useEffect(() => {
    const getData = async () => {
      const formattedDate = formatToYYYYMMDD(selectedDate);
      try {
        const response = await fetchMealsByDay(formattedDate);
        if (response) {
          const json = await response.json();
          console.log('json', json)
          setMealData(json);
          setActiveSections([0]);
          setIsLoaded(true);
        } else {
          // error handling
        }
      } catch (e) {
        // error handling
      }
    };

    if (selectedDate) {
      getData();
    }
  }, [selectedDate]);

  const renderHeader = (meal: MealData) => {
    return (
      <View style={styles.mealHeaderContainer}>
        <Text style={styles.mealHeaderText}>{meal.label}</Text>
      </View>
    );
  };

  const renderContent = (meal: MealData) => {
    return (
      <View style={styles.mealContentContainer}>
        <View>
          {/* <Image
            source="https://picsum.photos/seed/696/3000/2000"
            contentFit="cover"
            placeholder={{ blurhash }}
            style={{
              width: 100,
              height: 100
            }}
          /> */}
          <Text style={styles.mealContentText}>Contents:</Text>
          <Text>url: {meal.url}</Text>
          <Image source={meal.url} placeholder={{ blurhash }} style={{width: 100, height: 100}}/>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.scrollViewContainer}>
      {!isLoaded && <ActivityIndicator size="large" style={styles.indicator} />}
      {isLoaded && mealData && (
        <ScrollView>
          <Accordion
            sections={mealData}
            activeSections={activeSections}
            renderHeader={renderHeader}
            renderContent={renderContent}
            onChange={(sections) => {
              setActiveSections(sections);
            }}
          />
        </ScrollView>
      )}

      {isLoaded && !mealData && (
        <View style={styles.noImagesContainer}>
          <Text style={styles.noImagesText}>
            No Meals to view for this day, try logging a meal in the Home page
          </Text>
        </View>
      )}
    </View>
  );
}

export default function MealCalendar() {
  const currentDate = new Date();
  // for visualizing marks on days where meals were tracked
  const [trackedDays, setTrackedDays] = useState<MarkedDates>({});
  // currently selected date
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  // data is all pulled in from BE
  const [isLoaded, setIsLoaded] = useState(false);

  // populate information about meal data from current visible range of dates
  useEffect(() => {
    const getData = async () => {
      const tracked = await getTrackedDaysForMonth(currentDate);
      // select current day
      const currentDateFormatted = formatToYYYYMMDD(selectedDate);
      tracked[currentDateFormatted] = {
        ...(tracked[currentDateFormatted] || {}),
        ...{ selected: true, selectedColor: "lightblue" },
      };

      setTrackedDays(tracked);
    };

    getData();
    setIsLoaded(true);
  }, []);

  const getTrackedDaysForMonth = async (date: Date) => {
    const [start, end] = getRangeOfVisibleDates(date);
    let tracked: MarkedDates = {};
    try {
      const response = await fetchMealsByDates(
        formatToYYYYMMDD(start),
        formatToYYYYMMDD(end)
      );
      if (response) {
        const json = await response.json();
        tracked = formatTrackedDays(json);
      } else {
        // error handling
      }
    } catch (e) {
      // error handling
    }

    return tracked;
  };

  const formatTrackedDays = (data: { [key: string]: string }) => {
    // from tracked days -> convert to dots on calendar
    const tracked: MarkedDates = {};
    for (const [date, count] of Object.entries(data)) {
      const countInt = parseInt(count);
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

    return tracked;
  };

  const selectDay = (day: DateData) => {
    const currentTrackedDays = { ...trackedDays };
    const selectedDay = currentTrackedDays[day.dateString];

    const currentSelectedDay = selectedDate.toISOString().split("T")[0];
    // TODO might want to remove this and have a useEffect on selected date
    // and just handle that there?
    // might need to track prev selected date to
    // useful for figuring out if user can go to next month and not in future
    // need to ensure selected is property on this tracked -> see if trackedDays exists
    if (trackedDays[currentSelectedDay]?.selected) {
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

    setSelectedDate(new Date(day.year, day.month - 1, day.day));
    setTrackedDays(currentTrackedDays);
  };

  const monthChange = async (month: DateData) => {
    setIsLoaded(false);

    const currentSelectedMonth = new Date(month.dateString);

    // gather meal data for new range of visible days
    const tracked = await getTrackedDaysForMonth(currentSelectedMonth);

    const merged = { ...trackedDays };

    // get current selected date
    Object.keys(tracked).forEach((date) => {
      if (trackedDays[date]) {
        merged[date] = {
          ...tracked[date],
          ...trackedDays[date],
        };
      } else {
        merged[date] = {
          ...tracked[date],
        };
      }
    });

    setTrackedDays(merged);
    setIsLoaded(true);
  };

  const getRangeOfVisibleDates = (date: Date) => {
    // try and figure out the range of dates shown
    const selectedYear = date.getFullYear();
    const selectedMonth = date.getMonth();

    // get first day visible
    const firstDayOfMonth = new Date(selectedYear, selectedMonth, 1);
    const firstDayOfWeek = firstDayOfMonth.getDay();

    // go back to closest sunday
    const visibleStart = new Date(firstDayOfMonth);
    visibleStart.setDate(visibleStart.getDate() - firstDayOfWeek);

    // get last day visible
    const lastDayOfMonth = new Date(selectedYear, selectedMonth + 1, 0);
    const lastDayOfWeek = lastDayOfMonth.getDay();

    // go to next saturday
    const daysTillNextSaturday = 6 - lastDayOfWeek;
    const visibleEnd = new Date(lastDayOfMonth);
    visibleEnd.setDate(visibleEnd.getDate() + daysTillNextSaturday);

    return [visibleStart, visibleEnd];
  };

  const handleArrowLeft: (subtractMonth: () => void, month?: XDate) => void = (
    subtractMonth,
    month
  ) => {
    // select last day of this month
    const lastDayOfMonth = new Date(month!.getFullYear(), month!.getMonth(), 0);

    const lastDayFormatted = lastDayOfMonth.toISOString().split("T")[0];

    setSelectedDate(lastDayOfMonth);
    setTrackedDays({
      [lastDayFormatted]: { selected: true, selectedColor: "lightblue" },
    });

    // go to previous month
    subtractMonth();
  };

  const handleArrowRight: (addMonth: () => void, month?: XDate) => void = (
    addMonth,
    month
  ) => {
    // see if month is current month
    if (month!.getMonth() + 1 === currentDate.getMonth()) {
      setSelectedDate(currentDate);
      const currentDateFormatted = currentDate.toISOString().split("T")[0];
      setTrackedDays({
        [currentDateFormatted]: { selected: true, selectedColor: "lightblue" },
      });
    } else {
      // select first day of this month
      const firstDayOfMonth = new Date(
        month!.getFullYear(),
        month!.getMonth() + 1,
        1
      );

      const firstDayFormatted = firstDayOfMonth.toISOString().split("T")[0];

      setSelectedDate(firstDayOfMonth);
      setTrackedDays({
        [firstDayFormatted]: { selected: true, selectedColor: "lightblue" },
      });
    }

    // go to next month
    addMonth();
  };

  return (
    <View style={styles.container}>
      {/* <View style={styles.calendarContainer}> */}
      <Calendar
        maxDate={currentDate.toISOString().split("T")[0]}
        onDayPress={(day) => {
          selectDay(day);
        }}
        markingType={"multi-dot"}
        markedDates={trackedDays}
        testID={"calendar"}
        onMonthChange={monthChange}
        displayLoadingIndicator={!isLoaded}
        disableArrowRight={
          selectedDate.getFullYear() === currentDate.getFullYear() &&
          selectedDate.getMonth() === currentDate.getMonth()
        }
        onPressArrowLeft={handleArrowLeft}
        onPressArrowRight={handleArrowRight}
        style={styles.calendar}
      />
      {/* </View> */}
      <View style={styles.mealInfoContainer}>
        <MealInfoView selectedDate={selectedDate} />
        {/* TODO:Fix this portion for a test */}
        {/* <Text testID="date-text">
          {selectedDate.toISOString().split("T")[0]}
        </Text> */}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  mealInfoContainer: {
    flexGrow: 1,
  },
  indicator: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  scrollViewContainer: {
    flex: 1,
    marginTop: 5,
  },
  mealHeaderContainer: {
    alignItems: "center",
    paddingHorizontal: 4,
    paddingVertical: 8,
    marginHorizontal: 2,
    marginVertical: 8,
    borderColor: "black",
    borderWidth: 1,
  },
  mealHeaderText: {
    fontSize: 18,
  },
  noImagesContainer: {
    alignItems: "center",
    justifyContent: "center",
    paddingTop: 32,
    padding: 10,
  },
  noImagesText: {
    fontSize: 22,
  },
  mealContentContainer: {},
  mealContentText: {},
});
