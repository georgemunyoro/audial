<script>
  import Player from "./components/Player.svelte";
  import Sidebar from "./components/Sidebar.svelte";
  import TracksView from "./components/TracksView.svelte";
  import "./style/index.css";

  let currentlyActiveScreen = "tracks";
</script>

<main style="">
  <span style="display: flex;">
    <Sidebar
      {currentlyActiveScreen}
      onSidebarButtonClick={(id) => (currentlyActiveScreen = id)}
    />
    <TracksView display={currentlyActiveScreen == "tracks"} />
    <Player />
  </span>
</main>

<svelte:head>
  <link rel="stylesheet" href="./style/index.css" />
  <link rel="preconnect" href="https://fonts.gstatic.com" />
  <link
    href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200;0,300;0,400;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,600;1,700;1,800;1,900&display=swap"
    rel="stylesheet"
  />
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
    integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w=="
    crossorigin="anonymous"
  />
  <script
    type="text/javascript"
    src="https://cdn.jsdelivr.net/npm/amplitudejs@5.3.0/dist/amplitude.js"></script>
  <script
    src="https://cdn.jsdelivr.net/gh/foobar404/wave.js/dist/bundle.iife.js"></script>
</svelte:head>

<style>
  * {
    padding: 0;
    margin: 0;
    border: none;
  }
</style>
