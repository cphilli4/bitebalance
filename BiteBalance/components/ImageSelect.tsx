import { PropsWithChildren, useState, useEffect } from "react";
import {
  Button,
  Image,
  View,
  StyleSheet,
  TouchableOpacity,
  Modal,
  Text,
  Pressable,
  Alert,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { uploadImage } from "@/api/service";

import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

type Props = PropsWithChildren<{
  isVisible: boolean;
  onClose: () => void;
}>;


// Image Tracking Calendar
// want to be able to view tracked meals in a calendar view
  // need calendar component with ability to go forward and backward
  // want to display meals and progress for every day
    // show checkmark or x if day is not complete
  // require uploaded/imported images of meals to have a date
    // import - metadata from image?
    // upload - current date
    // store in database during upload
// when selected a day in the calendar want to view information for that day
  // show all meals uploaded for that day
  // allow for back uploading meals
  // show information from AI 

function ImageSelectModal({ isVisible, children, onClose }: Props) {
  return (
    <Modal animationType="slide" transparent={true} visible={isVisible}>
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <View style={styles.titleContainer}>
            <Text style={styles.title}>Upload this Image?</Text>
            <Pressable onPress={onClose} style={styles.closeButton}>
              <MaterialIcons name="close" color="fff" size={22} />
            </Pressable>
          </View>
          <View style={styles.childrenContainer}>{children}</View>
        </View>
      </View>
    </Modal>
  );
}

function SuccessMessage({ isVisible, children, onClose }: Props) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [isVisible]);

  return (
    <Modal transparent={false} visible={isVisible} animationType="fade">
      <View style={styles.modalContainer}>
        <View style={styles.successContainer}>
          <Text style={styles.successText}>Success!</Text>
        </View>
      </View>
    </Modal>
  );
}

export function ImageSelect() {
  const [image, setImage] = useState<ImagePicker.ImagePickerAsset | null>(null);
  const [showImageOptions, setShowImageOptions] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const selectImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0]);
      setShowImageOptions(true);
    } else {
      alert("You did not select an image.");
    }
  };

  const uploadPhoto = async () => {
    if (image) {
      let formData = new FormData();
      formData.append("meal", {
        uri: image.uri,
        name: image.fileName || "photo.jpg",
        type: "image/jpeg",
      } as any);
      formData.append("label", "a nice meal");
      const response = await uploadImage(formData);

      const json = await response?.json();
      setShowImageOptions(false);
      setShowSuccess(true);
    }
  };

  const cancelUpload = () => {
    setImage(null);
    setShowImageOptions(false);
  };

  return (
    <>
      {image && (
        <ImageSelectModal
          isVisible={showImageOptions}
          onClose={() => setShowImageOptions(false)}
        >
          <Image source={{ uri: image!.uri }} style={styles.image} />
          <View>
            <Pressable onPress={uploadPhoto} style={styles.confirmButton}>
              <Text style={styles.confirmText}>Confirm</Text>
            </Pressable>
          </View>
          <View>
            <Pressable onPress={cancelUpload} style={styles.cancelButton}>
              <Text style={styles.confirmText}>Cancel</Text>
            </Pressable>
          </View>
        </ImageSelectModal>
      )}
      <SuccessMessage
        isVisible={showSuccess}
        onClose={() => setShowSuccess(false)}
      />

      <TouchableOpacity style={styles.iconButton} onPress={selectImage} testID="image-select-button">
        <FontAwesome name="image" size={55} color="black" />
          <View style={styles.iconTextContainer}>
            <Text style={styles.iconText}>Select Image</Text>
          </View>
      </TouchableOpacity>
    </>
  );
}

const styles = StyleSheet.create({
  image: {
    width: 250,
    height: 250,
    borderRadius: 15,
    marginBottom: 20,
  },
  iconButton: {
    position: "absolute",
    bottom: 30,
    left: 30,
    padding: 15,
    borderRadius: 50,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    flexDirection: "row",
    alignItems: "center",
  },
  iconTextContainer: {
    flexDirection: "row",
    marginLeft: 15,
    alignItems: "center",
  },
  iconText: {
    fontSize: 16,
    fontWeight: "600",
    color: "black",
    marginRight: 5,
  },
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.7)",
  },
  modalContent: {
    width: "80%",
    borderRadius: 20,
    padding: 20,
    backgroundColor: "#f7f7f7",
    alignItems: "center",
  },
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    marginBottom: 15,
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
    color: "#1e3a5f",
  },
  closeButton: {
    backgroundColor: "#d1d5db",
    padding: 8,
    borderRadius: 20,
  },
  confirmButton: {
    backgroundColor: "#2563eb",
    padding: 10,
    borderRadius: 10,
    alignItems: "center",
    margin: 5,
  },
  cancelButton: {
    backgroundColor: "#d14343",
    padding: 10,
    borderRadius: 10,
    alignItems: "center",
    margin: 5,
  },
  confirmText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "white",
  },
  successContainer: {
    width: "60%",
    height: "20%",
    borderRadius: 20,
    backgroundColor: "#34d399",
    alignItems: "center",
    justifyContent: "center",
  },
  successText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
  },
  confirmText: {
    color: 'white'
  }
});
