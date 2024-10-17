

export const uploadImage = async (formData: FormData) => {
  try {
    const response = await fetch("http://192.168.64.1:8080/upload-meal-with-label", {
      method: "POST",
      body: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    console.log('inside res', response)
    return response;
  } catch (e) {
    console.log('uploadImage Error', e)
  }
};
