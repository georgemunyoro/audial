<script>
  import { onDestroy, onMount } from "svelte";
  import { currentTrack, queue, queuePosition } from "../store";
  import Track from "./Track.svelte";

  export let display = true;
  let search = "";
  let lastPlayed;

  const onTrackClick = (track) => {
    $queuePosition = $queue.findIndex((t) => track.id == t.id);
    $currentTrack = JSON.stringify(track);
    lastPlayed = track
  };

  const unsubscribeFromCurrentTrack = currentTrack.subscribe((value) => {
    let track;
    if (value) track = JSON.parse(value);
    else track = {}

    if (lastPlayed) {
      let oldTrackEl = document.getElementById(lastPlayed.id);
      if (oldTrackEl) {
        oldTrackEl.classList.toggle("active")
        // oldTrackEl.style.color = "black";
        // oldTrackEl.style.background = "#f4f2f0";
      }
      lastPlayed = track
    }

    let trackEl = document.getElementById(track.id);
    if (trackEl) {
      trackEl.classList.toggle("active")
      // trackEl.style.color = "white";
      // trackEl.style.background = "black";
    }
  });

  onDestroy(unsubscribeFromCurrentTrack);

  let tracks = [];
  let allTracks = [];

  onMount(async () => {
    const res = await fetch("http://localhost:8000/music?limit=2000");
    const data = await res.json();

    tracks = data;
    allTracks = data;

    $queue = data;
  });
</script>

<div
  class="tracks-view"
  style={`background: #f4f2f0; width: 80vw; height: calc(100vh - 66px); display: ${
    display ? "box" : "none"
  }`}
>
  <input
    on:input={(event) => {
      tracks = allTracks.filter(
        (track) =>
          track.title
            .toLowerCase()
            .includes(event.target.value.toLowerCase()) ||
          track.artist.toLowerCase().includes(event.target.value.toLowerCase())
      );

      let ct = JSON.parse($currentTrack);
      if (tracks.find((track) => track.id == ct.id)) {
        let trackEl = document.getElementById(JSON.parse($currentTrack).id);
        console.log(trackEl);
        trackEl.style.color = "white";
        trackEl.style.background = "black";
      }

      // try {
      //   let trackEl = document.getElementById(JSON.parse($currentTrack).id);
      //   console.log(trackEl)
      //   trackEl.style.color = "white";
      //   trackEl.style.background = "black";
      // } catch {}
    }}
    placeholder="Search..."
    class="tracks-search"
  />
  {#each tracks as track}
    <Track {track} onClick={onTrackClick} />
  {/each}
</div>

<style>
  .tracks-view {
    overflow-y: scroll;
  }

  .tracks-search {
    /* position: fixed; */
    width: 100%;
    background: #ccc;
    border: none;
    padding: 15px;
    font-size: 1.5rem;
    font-family: Nunito;
    font-weight: lighter;
  }


  :global(body.dark-mode) .tracks-view {
    background: #111 !important;
  }
  :global(body.dark-mode) .tracks-search {
    background: #222;
    color: white;
  }
</style>
