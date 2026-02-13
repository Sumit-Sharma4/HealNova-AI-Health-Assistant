function predictDisease() {

  // All symptom IDs (must match input.html + backend)
  const symptomIds = [
    "fever","headache","cough","body_pain","stomach_pain",
    "diarrhea","vomiting","sore_throat","runny_nose",
    "chest_pain","short_breath","skin_rash","itching",
    "acidity","back_pain","joint_pain","high_bp","low_bp","fatigue"
  ];

  // Allowed single-symptom cases (safe)
  const allowedSingleSymptoms = [
    "fatigue",
    "skin_rash",
    "cough",
    "headache"
  ];

  let data = {};
  let selectedSymptoms = [];

  // Collect symptom values
  symptomIds.forEach(symptom => {
    const checkbox = document.getElementById(symptom);
    const value = checkbox && checkbox.checked ? 1 : 0;
    data[symptom] = value;
    if (value === 1) selectedSymptoms.push(symptom);
  });

  const selectedCount = selectedSymptoms.length;

  // No symptom selected
  if (selectedCount === 0) {
    alert("Please select at least one symptom.");
    return;
  }

  // Unsafe single-symptom case
  if (
    selectedCount === 1 &&
    !allowedSingleSymptoms.includes(selectedSymptoms[0])
  ) {
    alert("Please select at least two symptoms for accurate prediction.");
    return;
  }

  // 🔄 Send data to backend
  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {

    //  Backend invalid input
    if (result.error) {
      alert(result.error);
      return;
    }

    // ✅ Store full prediction result for result.html
    localStorage.setItem("predictedDisease", result.predicted_disease);
    localStorage.setItem("diseaseType", result.disease_type);
    localStorage.setItem("specialist", result.specialist);
    localStorage.setItem("disclaimer", result.disclaimer);

    // Redirect to result page
    window.location.href = "result.html";
  })
  .catch(error => {
    console.error("Server error:", error);
    alert("Server error. Please try again later.");
  });
}

