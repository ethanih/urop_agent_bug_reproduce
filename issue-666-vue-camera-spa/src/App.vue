<template>
  <main class="app-shell">
    <section class="workspace" aria-label="Camera workspace">
      <div class="preview-panel">
        <video
          ref="videoEl"
          autoplay
          muted
          playsinline
          :class="['camera-feed', selectedFilter]"
          aria-label="Live camera preview"
        ></video>
        <canvas ref="canvasEl" class="capture-canvas" aria-hidden="true"></canvas>
        <div v-if="!streamActive" class="empty-state">
          <h1>Camera Filter Studio</h1>
          <p>Start the camera, choose a filter, capture a frame, then download it.</p>
        </div>
      </div>

      <aside class="controls" aria-label="Camera controls">
        <div class="control-row">
          <button class="primary" type="button" @click="startCamera" :disabled="streamActive">
            Start camera
          </button>
          <button type="button" @click="stopCamera" :disabled="!streamActive">
            Stop
          </button>
        </div>

        <fieldset>
          <legend>Filter</legend>
          <label v-for="filter in filters" :key="filter.value" class="filter-option">
            <input v-model="selectedFilter" type="radio" name="filter" :value="filter.value" />
            <span>{{ filter.label }}</span>
          </label>
        </fieldset>

        <div class="control-row">
          <button type="button" @click="captureFrame" :disabled="!streamActive">
            Capture
          </button>
          <a
            class="download"
            :class="{ disabled: !snapshotUrl }"
            :href="snapshotUrl || undefined"
            download="camera-filter-result.png"
            aria-disabled="!snapshotUrl"
          >
            Download
          </a>
        </div>

        <p v-if="errorMessage" class="error" role="alert">{{ errorMessage }}</p>
      </aside>
    </section>

    <section v-if="snapshotUrl" class="snapshot" aria-label="Captured result">
      <h2>Captured result</h2>
      <img :src="snapshotUrl" alt="Captured camera result with selected filter" />
    </section>
  </main>
</template>

<script setup>
import { onBeforeUnmount, ref } from 'vue';

const videoEl = ref(null);
const canvasEl = ref(null);
const selectedFilter = ref('filter-none');
const streamActive = ref(false);
const snapshotUrl = ref('');
const errorMessage = ref('');
let mediaStream = null;

const filters = [
  { label: 'None', value: 'filter-none' },
  { label: 'Mono', value: 'filter-mono' },
  { label: 'Warm', value: 'filter-warm' },
  { label: 'Cool', value: 'filter-cool' },
  { label: 'High contrast', value: 'filter-contrast' },
];

async function startCamera() {
  errorMessage.value = '';

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' },
      audio: false,
    });
    videoEl.value.srcObject = mediaStream;
    streamActive.value = true;
  } catch (error) {
    errorMessage.value = `Camera access failed: ${error.message}`;
  }
}

function stopCamera() {
  if (!mediaStream) {
    return;
  }

  mediaStream.getTracks().forEach((track) => track.stop());
  mediaStream = null;
  videoEl.value.srcObject = null;
  streamActive.value = false;
}

function captureFrame() {
  const video = videoEl.value;
  const canvas = canvasEl.value;

  if (!video || !canvas || !video.videoWidth || !video.videoHeight) {
    errorMessage.value = 'Camera is not ready yet.';
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext('2d');
  context.filter = cssFilterFor(selectedFilter.value);
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  if (snapshotUrl.value) {
    URL.revokeObjectURL(snapshotUrl.value);
  }

  canvas.toBlob((blob) => {
    if (!blob) {
      errorMessage.value = 'Could not create the image.';
      return;
    }
    snapshotUrl.value = URL.createObjectURL(blob);
  }, 'image/png');
}

function cssFilterFor(filterName) {
  const values = {
    'filter-none': 'none',
    'filter-mono': 'grayscale(1)',
    'filter-warm': 'sepia(0.35) saturate(1.25) hue-rotate(-8deg)',
    'filter-cool': 'saturate(1.2) hue-rotate(18deg)',
    'filter-contrast': 'contrast(1.45) saturate(1.2)',
  };

  return values[filterName] || 'none';
}

onBeforeUnmount(() => {
  stopCamera();
  if (snapshotUrl.value) {
    URL.revokeObjectURL(snapshotUrl.value);
  }
});
</script>
