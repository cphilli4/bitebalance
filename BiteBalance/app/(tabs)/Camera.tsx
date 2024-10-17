import { useState } from "react";
import { Button, Image, View, Text, StyleSheet } from "react-native";
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
  //     <ThemedView>
  //       <ThemedText>Give permission</ThemedText>
  //     </ThemedView>
  //   );
  // }

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera}>
        <ImageSelect />
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  camera: {
    flex: 1,
    backgroundColor: 'white'
  },
});
