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
            <Text style={styles.title}>Select this Image?</Text>
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

          <View style={styles.buttonContainer}>
            <Pressable onPress={cancelUpload} style={styles.cancelButton}>
              <Text style={styles.confirmText}>Cancel</Text>
            </Pressable>
            <Pressable onPress={uploadPhoto} style={styles.confirmButton}>
              <Text style={styles.confirmText}>Confirm</Text>
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
      </TouchableOpacity>
    </>
  );
}

const styles = StyleSheet.create({
  image: {
    width: 250,
    height: 250,
    borderRadius: 10,
    flexGrow: 1,
  },
  iconButton: {
    position: "absolute",
    bottom: 30,
    left: 30,
    backgroundColor: "white",
  },
  modalContainer: {
    height: "100%",
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalContent: {
    height: "75%",
    width: "75%",
    borderRadius: 25,
    padding: 10,
    backgroundColor: "grey",
  },
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 20,
  },
  title: {
    fontSize: 22,
  },
  closeButton: {
    alignItems: "center",
  },
  childrenContainer: {
    alignItems: "center",
    justifyContent: "center",
  },
  confirmButton: {
    borderWidth: 2,
    borderColor: "green",
    backgroundColor: "green",
    padding: 4,
    borderRadius: 4,
    paddingHorizontal: 6,
  },
  cancelButton: {
    borderWidth: 2,
    borderColor: "red",
    padding: 4,
    borderRadius: 4,
    paddingHorizontal: 6,
  },
  buttonContainer: {
    marginTop: 250,
    paddingHorizontal: 15,
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  successContainer: {
    width: "50%",
    height: "20%",
    borderRadius: 20,
    padding: 10,
    backgroundColor: "green",
    alignItems: 'center',
    justifyContent: 'center'
  },
  successText: {
    fontSize: 20,
    color: 'white',
    fontWeight: 'bold'
  },
  confirmText: {
    color: 'white'
  }
});
