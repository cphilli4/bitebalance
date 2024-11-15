import {
  SafeAreaView,
  StyleSheet
} from "react-native";

import Calendar from "@/components/MealCalendar"

export default function CalendarPage() {
  return (
    <SafeAreaView style={styles.container}>
      <Calendar />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  }
})

