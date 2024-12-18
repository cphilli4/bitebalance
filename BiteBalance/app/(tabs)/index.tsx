import { useState } from "react";
import {
  Button,
  Image,
  View,
  Text,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { CameraView, CameraType, useCameraPermissions } from "expo-camera";

import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";
import { ImageSelect } from "@/components/ImageSelect";

export default function Camera() {
  const [permission, requestPermission] = useCameraPermissions();

  // if (!permission) {
  //   return <View />;
  // }

  // if (!permission.granted) {
  //   return (
  //     // ask for camera permissions
  //     <SafeAreaView style={styles.container}>
  //       <ThemedView style={styles.grant}>
  //         <ThemedText>We need your permission to show the camera</ThemedText>
  //         <Button onPress={requestPermission} title="grant permission" />
  //       </ThemedView>
  //     </SafeAreaView>
  //   );
  // }

  return (
    <SafeAreaView style={styles.container}>
      <CameraView style={styles.camera}>
        <ImageSelect />
      </CameraView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
    backgroundColor: "white",
  },
  grant: {
    alignContent: 'center',
    justifyContent: 'center',
    flex: 1
  }
});
