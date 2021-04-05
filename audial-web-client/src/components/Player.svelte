<script>
  import { onDestroy } from "svelte";
  import { currentTrack, queue, queuePosition } from "../store";

  const audio = new Audio();

  let currentTrackUrl = "";
  let currentTrackArt = "";
  let paused = audio.paused;
  let progress = 0;
  let shuffle = false;
  let prevQueuePositions = [];

  const handleNewTrack = async (track) => {
    audio.pause();
    paused = true;
    const res = await fetch("http://localhost:8000/music/" + track.id);

    const trackData = await res.json();
    currentTrackArt = trackData.art;
    currentTrackUrl = trackData.track;

    audio.src = currentTrackUrl;
    audio.play();
    paused = false;
  };

  const unsubscribeFromCurrentTrack = currentTrack.subscribe((value) => {
    if (value) handleNewTrack(JSON.parse(value));
  });

  const unsubscribeFromQueuePosition = queuePosition.subscribe((value) => {
    $currentTrack = JSON.stringify($queue[$queuePosition]);
  });

  onDestroy(unsubscribeFromQueuePosition);
  onDestroy(unsubscribeFromCurrentTrack);

  const playPause = () => {
    if (audio.paused) audio.play();
    else {
      audio.pause();
    }
    paused = audio.paused;
  };

  const nextTrack = () => {
    prevQueuePositions.push($queuePosition)
    if (shuffle) {
      $queuePosition = Math.floor(Math.random() * $queue.length);
      return;
    }
    if ($queuePosition < $queue.length) $queuePosition++;
  };

  const prevTrack = () => {
    $queuePosition = prevQueuePositions.pop();
    // if ($queuePosition > 0) $queuePosition--;
  };

  const handleProgressBarClick = (event) => {
    const timeToSet = (audio.duration / 100) * event.target.value;
    audio.currentTime = timeToSet;
  };

  audio.ontimeupdate = () => {
    progress = (100 / audio.duration) * audio.currentTime;
  };

  audio.onended = nextTrack;
</script>

<div class="player">
  <div class="controls">
    <img width="50" src={currentTrackArt} alt="" />
    <div style="display: flex;" class="player-track">
      {#if $currentTrack}
        <p style="font-family: Nunito; font-weight: lighter">
          {JSON.parse($currentTrack).title}·
        </p>
        <p style="font-family: Nunito; font-weight: bold">
          {JSON.parse($currentTrack).artist}
        </p>
      {/if}
    </div>

    <div>
      <input
        class="slider player-progress"
        type="range"
        width="100"
        value={`${progress}`}
        on:input={handleProgressBarClick}
      />
    </div>

    <span>
      <button class="shuffle-button" on:click={() => (shuffle = !shuffle)}
        ><i
          style={`color: ${shuffle ? "royalblue" : "silver"}`}
          class="fa fa-random"
        /></button
      >
      <button class="prev-button" on:click={prevTrack}
        ><i class="fa fa-angle-left" /></button
      >
      <button class="play-button" on:click={playPause}>
        {#if paused == true}
          <i class="fa fa-play" />
        {:else if paused == false}
          <i class="fa fa-pause" />
        {/if}
      </button>
      <button class="next-button" on:click={nextTrack}
        ><i class="fa fa-angle-right" /></button
      >
    </span>

    <!-- <div>
      <button><i class="fa fa-volume-off" /></button>
      <input type="range" />
    </div> -->
  </div>
</div>

<style>
  .player {
    position: absolute !important;
    bottom: 0;
    width: 100%;
    background: #eee;
    height: 66px;
    border-top: 2px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: right;
  }

  .controls {
    display: grid;
    grid-template-columns: 80px max-content auto 192px !important;
    width: 100%;
    padding: 0 1rem;
    align-items: center;
  }

  .play-button {
    /* background: #eee; */
    /* border-radius: 50%; */
    border: none;
    width: 40px;
    height: 40px;
    /* color: black; */
    font-size: 1.5rem;
  }

  .next-button {
    border: none;
    background: #eee;
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
  }

  .prev-button {
    border: none;
    background: #eee;
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
  }

  .shuffle-button {
    border: none;
    background: #eee;
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
    margin-left: 1rem;
  }

  .player-progress {
    width: 100%;
    padding: 2rem;
    /* margin-right: 22em; */
  }

  img {
    /* position: absolute;
    bottom: 7px;
    left: 7px; */
    border-radius: 5px;
  }


  :global(body.dark-mode) .player-track {
    color: white !important;
  }

  :global(body.dark-mode) .player {
    background: #222;
    border-top: none;
  }

  :global(body.dark-mode) .controls > span > button {
    background: none;
  }
</style>
