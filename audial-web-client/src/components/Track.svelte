<script>
  import Button from "./Button.svelte";

  export let track;
  export let onClick = () => {};
</script>

<div class="track" id={track.id} on:click={() => onClick(track)}>
  <p class="track-title">{track.title}</p>
  <p class="track-artist">{track.artist}</p>
</div>

<style>
  .track {
    font-family: Nunito;
    width: 100%;
    border-bottom: 1px solid #eee;
    padding: 0.5rem 15px;
    align-items: center;
    cursor: pointer;
  }

  .track:nth-child(1) {
    margin-top: 3.9rem;
  }

  .track:hover {
    background: #eee;
  }

  .track-title {
    font-weight: bold;
  }

  .track-artist {
    font-weight: lighter;
  }

  :global(body.dark-mode) .track-title {
    color: #08d58f;
  }

  :global(body.dark-mode) .track-artist {
    color: white;
  }

  :global(body.dark-mode) .track {
    background: #53354a;
    border-bottom: none;
    background: #111;
  }

  :global(body.dark-mode) .track.active {
    border: 1px solid red !important;
    background: red !important;
  }
</style>
