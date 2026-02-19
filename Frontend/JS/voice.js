/* ==================================
   🎤 VOICE INPUT (Speech → Text)
================================== */

let recognition;
let isListening = false;

function startListening() {

  if (!('webkitSpeechRecognition' in window)) {
    alert("Voice input not supported in this browser.");
    return;
  }

  const micBtn = document.getElementById("micBtn");

  if (isListening) {
    stopVoice();
    return;
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-IN";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = function () {
    isListening = true;
    micBtn.classList.add("listening");
    micBtn.innerText = "🎙 Listening...";
  };

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("question").value = transcript;
  };

  recognition.onend = function () {
    isListening = false;
    micBtn.classList.remove("listening");
    micBtn.innerText = "🎤 Start Listening";
  };

  recognition.onerror = function () {
    isListening = false;
    micBtn.classList.remove("listening");
    micBtn.innerText = "🎤 Start Listening";
    alert("Voice recognition error.");
  };

  recognition.start();
}

/* ==================================
   🔊 VOICE OUTPUT (Text → Speech)
================================== */

async function speakAnswer() {
  const replyText = document.getElementById("reply").innerText;

  if (!replyText || replyText.includes("Ask a question")) {
    alert("No AI reply to speak.");
    return;
  }

  const selectedLang =
    document.querySelector('input[name="voiceLang"]:checked').value;

  let textToSpeak = replyText;

  // 🔥 If Hindi selected → Translate first
  if (selectedLang === "hi") {
    textToSpeak = await translateToHindi(replyText);
  }

  const speech = new SpeechSynthesisUtterance(textToSpeak);
  speech.lang = selectedLang === "hi" ? "hi-IN" : "en-US";
  speech.rate = 1;
  speech.pitch = 1;

  window.speechSynthesis.speak(speech);
}
async function translateToHindi(text) {
  try {
    const res = await fetch("https://healnova-backend.onrender.com/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    });

    const data = await res.json();
    return data.translated || text;

  } catch (error) {
    console.error("Translation error:", error);
    return text;
  }
}



/* ==================================
   🔇 STOP (Listening + Speaking)
================================== */

function stopVoice() {

  if (recognition && isListening) {
    recognition.stop();
    isListening = false;
  }

  window.speechSynthesis.cancel();
}
